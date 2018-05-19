#include <Keypad.h>
#include <EEPROM.h>
#define SIZE_BUFFER_DATA 50

//Button pin
const int CONTACT_PIN = 11;

//R LED pin
const int R_LED_PIN = 13;

//G LED pin
const int G_LED_PIN = 12;

//B LED pin
const int B_LED_PIN = 10;

const String boardId = "Arduino007";

//----------------------------------

char bufferData[SIZE_BUFFER_DATA];

const String KEY[] = {"3141", "2718", "1234"};

String inputString = "";

const byte ROWS = 4;

const byte COLS = 3;

const byte maxAttempts = 3;

int pirPin = 2;

int bateria = A2;

int ledPresencia = A1;

int ledBateria = A0;

int pirState = LOW;

int batteryState = LOW;

int valorPIR;

int valorBateria;

long temporizadorBateria;

bool fallaBateria = false;

long contadorFallaBateria;

bool bateriaBaja = false;

boolean stringComplete = false;

String firstVal = "";

String secondVal = "";

long currTime;

long timeConfirmacion;

long timeHealthcheck = 0;

const int tiempoTimeout = 5000;

const int tiempoHealthcheck = 10000;

boolean esperandoConfirmacion = false;

boolean confirmado = false;

boolean cerrar = false;

boolean intentoFallido = false;

//Keypad mapping matrix
char hexaKeys[ROWS][COLS] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}};

//Keypad row pins definition
byte rowPins[ROWS] = {
    9, 8, 7, 6};

//Keypad column pins definition
byte colPins[COLS] = {
    5, 4, 3};

//Keypad library initialization
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

//Current key variable
String currentKey;
//Door state
boolean permitidoEntrar;
//Number of current attempts
byte attempts;

//State Machine
const int STAND_BY = 0;
const int PUERTA_ABIERTA_BOTON = 1;
const int ERROR_PUERTA_ABIERTA_BOTON = 2;
const int PUERTA_ABIERTA_TECLADO = 3;
const int ERROR_PUERTA_ABIERTA_TECLADO = 4;
const int BLOQUEADO = 5;

int estado;

//-----------------------------------

void setColor(int redValue, int greenValue, int blueValue)
{
  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}

//-----------------------------------

// Method that compares a key with stored keys
boolean compareKey(String key)
{
  int acc = 3;
  int codif, arg0, arg1;
  for (int i = 0; i < 3; i++)
  {
    codif = EEPROM.read(i);
    while (codif != 0)
    {
      if (codif % 2 == 1)
      {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc + 1) * 256;
        arg1 += arg0;
        if (String(arg1) == key)
        {
          return true;
        }
      }
      acc += 2;
      codif >>= 1;
    }
    acc = (i + 1) * 16 + 3;
  }
  return false;
}

// Methods that divides the command by parameters
void processCommand(String input)
{
  boolean band = false;
  for (int i = 0; i < input.length(); i++)
  {
    if (input.substring(i, i + 1) == ";")
    {
      firstVal = input.substring(0, i);
      secondVal = input.substring(i + 1);
      band = true;
      break;
    }
  }
  if (!band)
  {
    firstVal = input;
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index)
{
  byte arg0 = val % 256;
  byte arg1 = val / 256;
  EEPROM.write((index * 2) + 3, arg0);
  EEPROM.write((index * 2) + 4, arg1);
  byte i = 1;
  byte location = index / 8;
  byte position = index % 8;
  i <<= position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location, j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index)
{
  byte arg0 = val % 256;
  byte arg1 = val / 256;
  EEPROM.write((index * 2) + 3, arg0);
  EEPROM.write((index * 2) + 4, arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index)
{
  byte i = 1;
  byte location = index / 8;
  byte position = index % 8;
  i <<= position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location, j);
}

//Method that deletes all passwords
void deleteAllPasswords()
{
  //Password reference to inactive
  EEPROM.write(0, 0);
  EEPROM.write(1, 0);
  EEPROM.write(2, 0);
}

//-----------------------------------

void setup()
{
  Serial.begin(9600);
  inputString.reserve(100);

  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN, INPUT);
  pinMode(ledPresencia, OUTPUT);
  pinMode(pirPin, INPUT);

  currentKey = "";
  permitidoEntrar = false;
  attempts = 0;

  estado = STAND_BY;

  setColor(0, 0, 255);
}

void loop()
{
  //Healthcheck

  if (millis() - timeHealthcheck > tiempoHealthcheck)
  {
    timeHealthcheck = millis();
    Serial.println(boardId+"\t5");
  }

  //PIR
  valorPIR = digitalRead(pirPin);
  if (valorPIR > 0)
    analogWrite(ledPresencia, 200);
  else
    analogWrite(ledPresencia, 0);
  if (pirState != valorPIR)
  {
    pirState = valorPIR;
    if (valorPIR == HIGH && !permitidoEntrar)
    {
      Serial.println(boardId + "\t3");
    }
  }

  //===================================================================

  //Bateria
  valorBateria = analogRead(bateria);
  float voltage = valorBateria * (5.4 / 1023.0);
  //Bateria Alta
  if (voltage > 1.2)
  {
    analogWrite(ledBateria, 0);
    if (bateriaBaja)
    {
      delay(150);
    }
    bateriaBaja = false;
    batteryState = LOW;
    fallaBateria = false;
  }
  //Bateria baja
  else
  {
    analogWrite(ledBateria, 200);
    //Primera vez que se ingresa
    if (!bateriaBaja)
    {
      Serial.println(boardId + "\t4");
      bateriaBaja = true;
      delay(150);
    }
    //Si la batería es baja y han pasado más de 30 segs desde la última vez que se tocó la alarma
    if (batteryState == LOW && !fallaBateria)
    {
      temporizadorBateria = millis();
      contadorFallaBateria = millis();
      fallaBateria = true;
    }
    //Espera 30 segundos para volver a poner el Led de alarma
    else if (batteryState == HIGH)
    {
      //Si la batería es baja y han pasado 30 segs desde la última vez que se tocó la alarma
      if (millis() - temporizadorBateria >= 30000)
      {
        contadorFallaBateria = millis();
        batteryState = LOW;
      }
    }
    //Si se debe poner el Led como rojo
    else if (fallaBateria)
    {
      setColor(255, 0, 0);
      if (millis() - contadorFallaBateria >= 2000)
      {
        fallaBateria = false;
        batteryState = HIGH;
      }
    }
  }

  //===================================================================

  while (Serial.available())
  {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n')
    {
      stringComplete = true;
    }
  }

  if (stringComplete)
  {
    inputString = inputString.substring(0, inputString.length() - 1);
    processCommand(inputString);
    firstVal.trim();
    if (firstVal == "ABRIR")
    {
      confirmado = true;
    }
    else if (firstVal == "CERRAR")
    {
      cerrar = true;
    }
    else if (firstVal == "NEW_PASSWORD")
    {
      processCommand(secondVal);
      addPassword(secondVal.toInt(), firstVal.toInt());
    }
    else if (firstVal == "CHANGE_PASSWORD")
    {
      processCommand(secondVal);
      updatePassword(secondVal.toInt(), firstVal.toInt());
    }
    else if (firstVal == "DELETE_PASSWORD")
    {
      deletePassword(secondVal.toInt());
    }
    else if (firstVal == "DELETE_ALL")
    {
      deleteAllPasswords();
    }
    inputString = "";
    stringComplete = false;
  }

  //===================================================================

  //Lecturas
  //BOTON
  int button = digitalRead(CONTACT_PIN);
  char customKey;
  //KEYPAD
  customKey = customKeypad.getKey();

  //Transiciones y salidas
  switch (estado)
  {
  //Estado Stand_by
  case STAND_BY:
    permitidoEntrar = false;
    if (!fallaBateria && !esperandoConfirmacion)
      setColor(0, 0, 255);
    //Botón oprimido
    if (button == 1)
    {
      estado = PUERTA_ABIERTA_BOTON;
      permitidoEntrar = true;
      esperandoConfirmacion = false;
      currTime = millis();
      currentKey = "";
      attempts = 0;
    }
    //Leer número

    if (confirmado)
    {
      
      if(esperandoConfirmacion) {
        estado = PUERTA_ABIERTA_TECLADO;
        permitidoEntrar = true;
        setColor(0, 255, 0);
        attempts = 0;
        currTime = millis();
      }
      esperandoConfirmacion = false;
      confirmado = false;
    }

    if (cerrar)
    {
      if(esperandoConfirmacion) {
        Serial.println("denegado");
        intentoFallido = true;
        
      }
      esperandoConfirmacion = false;
      cerrar = false;
    }

    if (esperandoConfirmacion && millis() - timeConfirmacion > tiempoTimeout)
    {
      esperandoConfirmacion = false;
      setColor(255, 0, 255);
      delay(1000);
      setColor(0, 0, 255);
    }

    if (intentoFallido)
    {
      Serial.println("intento Fallido " + intentoFallido);
      intentoFallido = false;
      attempts = attempts + 1;
      setColor(255, 0, 0);
      //Máximo número de intentos incorrectos
      if (attempts >= maxAttempts)
      {

        estado = BLOQUEADO;
        Serial.println(boardId + "\t2");
        attempts = 0;
        currTime = millis();
      }
      //Un intento incorrecto
      else
      {
        delay(1000);
      }
    }

    if (customKey && customKey != '*' && customKey != '#' && !esperandoConfirmacion)
    {
      currentKey += String(customKey);
    }

    //Reiniciar Clave
    else if (customKey && customKey == '#')
    {
      currentKey = "";
    }
    //Se ingresó clave
    else if (currentKey.length() == 4)
    {
      //verificar clave
      boolean comparacion = compareKey(currentKey);

      if (comparacion)
      {
        //Serial.println("comparacion Correcta");
        currentKey = "";
        comparacion = false;
        timeConfirmacion = millis();
        Serial.println(boardId+"\t+"'0'+"\t"+tiempoTimeout+"\t"+currentKey);
        esperandoConfirmacion = true;
        setColor(255, 255, 255);
      }
      else
      {
        intentoFallido = true;
      }

      currentKey = "";
      //Clave incorrecta
    }
    break;
  //Estado Puerta abierta botón
  case PUERTA_ABIERTA_BOTON:
    if (!fallaBateria)
      setColor(0, 255, 0);
    //Se dejó de oprimir el botón
    if (button == 0)
    {
      estado = STAND_BY;
    }
    //Se supperó el tiempo de puerta abierta
    else if (millis() - currTime > 30000)
    {
      estado = ERROR_PUERTA_ABIERTA_BOTON;
      permitidoEntrar = false;
      Serial.println(boardId + "\t1");
    }
    break;
    //Estado error puerta abierta botón
  case ERROR_PUERTA_ABIERTA_BOTON:
    setColor(255, 0, 0);
    //Se dejó de oprimir el botón
    if (button == 0)
    {
      estado = STAND_BY;
    }
    break;
    //Estado puerta abierta teclado
  case PUERTA_ABIERTA_TECLADO:
    if (!fallaBateria)
      setColor(0, 255, 0);
    //Se cerró la puerta
    if (customKey && customKey == '*')
    {
      estado = STAND_BY;
    }
    //Se supperó el tiempo de puerta abierta
    else if (millis() - currTime > 30000)
    {
      estado = ERROR_PUERTA_ABIERTA_TECLADO;
      permitidoEntrar = false;
      Serial.println(boardId + "\t1");
    }
    break;
  //Estado error puerta abierta teclado
  case ERROR_PUERTA_ABIERTA_TECLADO:
    setColor(255, 0, 0);
    //Se cerró la puerta
    if (customKey && customKey == '*')
    {
      estado = STAND_BY;
    }
    break;
  case BLOQUEADO:
    setColor(255, 0, 0);
    if (millis() - currTime > 30000)
    {
      estado = STAND_BY;
    }
    break;
  }
}

