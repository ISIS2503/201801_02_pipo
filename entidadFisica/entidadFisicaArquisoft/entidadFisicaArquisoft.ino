#include <Keypad.h>

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

const String KEY[] = {"3141","2718","1234"};

const byte ROWS = 4;

const byte COLS = 3;

const byte maxAttempts = 3;

int pirPin = 2;

int bateria= A0;

int ledPresencia = A1;

int ledBateria = A2;

int pirState = LOW;

int val;

long currTime;

//Keypad mapping matrix
char hexaKeys[ROWS][COLS] = {
  {
    '1', '2', '3'
  }
  ,
  {
    '4', '5', '6'
  }
  ,
  {
    '7', '8', '9'
  }
  ,
  {
    '*', '0', '#'
  }
};

//Keypad row pins definition
byte rowPins[ROWS] = {
  9, 8, 7, 6
}; 

//Keypad column pins definition
byte colPins[COLS] = {
  5, 4, 3
};

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

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}

void setup() {
  Serial.begin(9600);
  
  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN,INPUT);
  pinMode(ledPresencia, OUTPUT);
  pinMode(pirPin, INPUT);

  currentKey = "";
  permitidoEntrar = false;
  attempts = 0;

  estado = STAND_BY;
  
  setColor(0, 0, 255);
}

void loop() {
  //PIR
  val = digitalRead(pirPin);
  if(val>0)
     analogWrite(ledPresencia, 200);
  else
    analogWrite(ledPresencia, 0);
  if(pirState != val) {
    pirState = val;
    if(val == HIGH && !permitidoEntrar) {
      Serial.println(boardId+"\t3");
    }
  }

  //===================================================================

  //Bateria
  int valBateria = analogRead(bateria);
  float voltage = valBateria * (5.0 / 1023.0);
  if(voltage>1.2)
     analogWrite(ledBateria, 0);
  else
    analogWrite(ledBateria, 200);
  if(voltage<1.2) {
    //Serial.println(boardId+"\t4");
  }

  //===================================================================
  
  //Lecturas
  //BOTON
  int button = digitalRead(CONTACT_PIN);
  char customKey;
  //KEYPAD
  customKey = customKeypad.getKey();
  

  //Transiciones y salidas
  switch(estado) {
    //Estado Stand_by
    case STAND_BY:
      permitidoEntrar = false;
      setColor(0, 0, 255);
      //Botón oprimido
      if(button == 1) {
        estado = PUERTA_ABIERTA_BOTON;
        permitidoEntrar=true;
        currTime = millis();
        currentKey = "";
        attempts = 0;
      }
      //Leer número
      if (customKey && customKey!='*' && customKey!='#') {  
        currentKey+=String(customKey);
      }
      //Reiniciar Clave
      else if(customKey && customKey=='#')
      {
        currentKey = "";
      }
      //Se ingresó clave
      else if(currentKey.length()==4)
      {
        //verificar clave
        for(int i = 0; i<sizeof(KEY); i++) {
          if(currentKey == KEY[i]) {
            estado = PUERTA_ABIERTA_TECLADO;
            
            permitidoEntrar = true;
            setColor(0, 255, 0);
            attempts = 0;
            currTime = millis();
          }
        }
        currentKey = "";
        //Clave incorrecta
        if(!permitidoEntrar) {    
          attempts = attempts + 1;
          setColor(255, 0, 0);
          //Máximo número de intentos incorrectos 
          if(attempts >= maxAttempts){ 
                                 
            estado=BLOQUEADO;
            Serial.println(boardId+"\t2");
            attempts=0;
            currTime = millis();
          }
          //Un intento incorrecto
          else
          {
            delay(1000);
          }
        }
      }
      break;
    //Estado Puerta abierta botón
    case PUERTA_ABIERTA_BOTON:
      setColor(0, 255, 0);
      //Se dejó de oprimir el botón
      if(button==0){        
        estado=STAND_BY;
      }
      //Se supperó el tiempo de puerta abierta
      else if(millis()-currTime>30000)
      {
         estado=ERROR_PUERTA_ABIERTA_BOTON;
        permitidoEntrar=false;
         Serial.println(boardId+"\t1");
      }
      break;
      //Estado error puerta abierta botón
    case ERROR_PUERTA_ABIERTA_BOTON:
        setColor(255, 0, 0);
         //Se dejó de oprimir el botón
         if(button==0){
          estado=STAND_BY;
      }
      break;
      //Estado puerta abierta teclado
    case PUERTA_ABIERTA_TECLADO:
        setColor(0, 255, 0);
         //Se cerró la puerta
        if (customKey && customKey=='*') {  
        estado=STAND_BY;
        }
        //Se supperó el tiempo de puerta abierta
        else if(millis()-currTime>30000)
        {
         estado=ERROR_PUERTA_ABIERTA_TECLADO;
          permitidoEntrar=false;
         Serial.println(boardId+"\t1");
        }
       break;
    //Estado error puerta abierta teclado
    case ERROR_PUERTA_ABIERTA_TECLADO:
      setColor(255, 0, 0);
      //Se cerró la puerta
      if (customKey && customKey=='*') {  
        estado=STAND_BY;
        }
        break;
     case BLOQUEADO:
      setColor(255, 0, 0);
      if(millis()-currTime>30000)
        {
         estado=STAND_BY;
        }
      break;
    }
}  
