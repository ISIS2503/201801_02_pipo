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

const long timeBlock = 10000;

//---------------------------------- 

const String KEY = "3141";

const byte ROWS = 4;

const byte COLS = 3;

const byte maxAttempts = 3;

boolean openKeypad;

boolean keypadState;

long currTimeKeypad;

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
boolean open;
//Number of current attempts
byte attempts;
//If the number of current attempts exceeds the maximum allowed
boolean block;

//-----------------------------------
int pirPin = 2;

int redLed = 1;

int pirState = LOW;

int val;

boolean openTooMuchTime;


//Attribute that defines the button state
boolean buttonState;

//Current time when the button is tapped
long currTimeButton;

void setup() {
  Serial.begin(9600);
  buttonState = false;
  
  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN,INPUT);
  pinMode(redLed, OUTPUT);
  pinMode(pirPin, INPUT);

  currentKey = "";
  open = false;
  openKeypad = false;
  keypadState = false;
  attempts = 0;
  block = false;
  
  setColor(0, 0, 255);
}

void loop() {
  //PIR
  val = digitalRead(pirPin);
  digitalWrite(redLed, val);
  if(pirState != val) {
    pirState = val;
    if(val == HIGH) {
      Serial.println(boardId+"\t3");
    }
  }

  //===================================================================
  
  //KEYPAD

  char customKey;

   //If door is openned
  if(openKeypad) {
    if(millis()-currTimeKeypad >= timeBlock) {
      setColor(255, 0, 0);
      if(!keypadState) {
        keypadState = true;
        Serial.println(boardId+"\t1");
      }
    }
    //If the current key contains '*' and door is open
    if(currentKey.endsWith("*")) {
      openKeypad = false;
      keypadState = false;
      setColor(0, 0, 255);
      currentKey = "";
    }
  }
  
  if(!block && !openKeypad) {
    //Selected key parsed;
    customKey = customKeypad.getKey();
  }
  else {
    block = millis()- currTimeKeypad < timeBlock;
    if(!block){
      setColor(0, 0, 255);
    }
  }

  //Verification of input and appended value
  if (customKey) {  
    currentKey+=String(customKey);
  }

 
  //If the current key contains '#' reset attempt
  if(currentKey.endsWith("#")&&currentKey.length()<=KEY.length()) {
    currentKey = "";
  }

  //If current key matches the key length
  if (currentKey.length()== KEY.length()) {
    if(currentKey == KEY) {
      currentKey = "";
      openKeypad = true;
      setColor(0, 255, 0);
      attempts = 0;
      currTimeKeypad = millis();
    }
    else {
      attempts++;
      currentKey = "";
      setColor(255, 0, 0);
      delay(1000);
      setColor(0, 0, 255);
    }
  }
  if(attempts>=maxAttempts && !block) {
    block = true;
    setColor(255, 0, 0);
    currTimeKeypad = millis();
    attempts = 0;
    Serial.println(boardId+"\t2");
    
  }
  
  //===================================================================
  
  //Security Contact
  
  // put your main code here, to run repeatedly:
  //Button input read and processing 
  if(!buttonState) {
    if(digitalRead(CONTACT_PIN)) {
      currTimeButton = millis();
      buttonState = true;
      setColor(0, 255, 0);
      open = true;
      attempts = 0;
    }
  }
  else {
    if(digitalRead(CONTACT_PIN)) {
      if((millis()-currTimeButton)>=timeBlock) {
        setColor(255, 0, 0);
        if(!openTooMuchTime) {
          openTooMuchTime = true;
          Serial.println(boardId+"\t1");
        }
      }
    }else{
      setColor(0, 0, 255);
      open = false;
      buttonState = false;
    }
  }
  delay(100);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}
