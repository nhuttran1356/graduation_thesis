#include "Arduino.h"
#include "max6675.h"
#include <TimerOne.h>
#include <SoftwareSerial.h>


MAX6675 thermocouple(SCK1, CS, SO);

const byte RX = 8;
const byte TX = 9;
SoftwareSerial mySerial = SoftwareSerial(RX, TX);
String dataSend = "";


#define TRIAC_PIN 7
#define A1 15 
int SO = 4;
int CS = 5;
int SCK1 = 6;

#define Kp 0.0176
#define Ki 0.000117
#define Kd 0



float nhietdodat;

float nhietdo;
float t;

float E, E1, E2, alpha, gamma_value, beta;
float Output = 0;
float LastOutput = 0;
float thoigian = 0;

float T = 1500;  //Sample time 1.5s
float timerloop;

float tam = 0;


// servo
const int pin13 = 13;
const int pin12 = 12;

//
const long interval = 1000;
unsigned long previousMillis = 0;
int maxHeight = 22;   // Max Height
int minHeight = 0;    // Min Height
int waterLevel1 = 0;  
int waterLevel2 = 0;  

int setWater1;
int setWater2;
int setTemp;



// ----------

/*Function read Temp*/


void Temperature() {
  float read_ADC;
  nhietdo = readTemperature();
}

/*Control TRIAC*/
void TriacControl() {
  delayMicroseconds(thoigian * 1000);
  digitalWrite(TRIAC_PIN, HIGH);
  delay(1);
  digitalWrite(TRIAC_PIN, LOW);
}

void PID() {
  for (int i = 0; i < 10; i++) {
    Temperature();
    tam += nhietdo;
  }
  nhietdo = tam / 10.0;
  tam = 0;
  E = nhietdodat - nhietdo;
  alpha = 2 * T * Kp + Ki * T * T + 2 * Kd;
  beta = T * T * Ki - 4 * Kd - 2 * T * Kp;
  gamma_value = 2 * Kd;
  Output = (alpha * E + beta * E1 + gamma_value * E2 + 2 * T * LastOutput) / (2 * T);

  LastOutput = Output;
  E2 = E1;
  E1 = E;
  if (Output > 9)
    Output = 9;
  else if (Output <= 1)
    Output = 1;
  thoigian = 10 - Output; /***************/
  waterLevel_Temp();
}
// --------
long readUltrasonicDistance(int triggerPin, int echoPin) {
  pinMode(triggerPin, OUTPUT);  
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);

  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);

  return pulseIn(echoPin, HIGH);
}

void setup() {
 
  Serial.begin(9600);
  mySerial.begin(9600);

  //servo
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(A0, OUTPUT);

  //Temp
  pinMode(CS, OUTPUT);
  pinMode(SCK1, OUTPUT);
  pinMode(SO, INPUT);

  digitalWrite(CS, HIGH);
  //-----
  
  pinMode(TRIAC_PIN, OUTPUT);
  E = 0;
  E1 = 0;
  E2 = 0;
  attachInterrupt(0, TriacControl, RISING);
  Timer1.initialize(1500000);  //don vi us 1500000 = 1.5s
  Timer1.attachInterrupt(PID);


}



void loop() {
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\r');
    char firstChar = data.charAt(0);
    Serial.println(firstChar);

    switch (firstChar) {
      case 'A':
         digitalWrite(A0, HIGH);
        break;

      case 'B':
         digitalWrite(A0, LOW);
        break;

      case 'N':
        // noInterrupts();
        Timer1.stop();
        onServo();
        // interrupts();
        Timer1.start();
        break;

      case 'C':
        int commaIndex1 = data.indexOf(',');
        String temperatureData = data.substring(commaIndex1 + 1);
        int commaIndex2 = temperatureData.indexOf(',');
        String temperatureStr = temperatureData.substring(0, commaIndex2);
        String waterLevelStr = temperatureData.substring(commaIndex2 + 1);

        int setTemp = temperatureStr.toInt();

        // split data
        int commaIndex3 = waterLevelStr.indexOf(',');
        String waterLevelStr1 = waterLevelStr.substring(0, commaIndex3);
        String waterLevelStr2 = waterLevelStr.substring(commaIndex3 + 1);

        // tank1
        setWater1 = waterLevelStr1.toInt();

        // tank2
        setWater2 = waterLevelStr2.toInt();
 	      nhietdodat = temperatureStr.toInt(); 

        Serial.print("Received Temperature: ");
        Serial.println(nhietdodat);
        Serial.print("Received Water Level 1: ");
        Serial.println(setWater1);
        Serial.print("Received Water Level 2: ");
        Serial.println(setWater2);

        break;
      default:
        break;
    }
  }


}


void waterLevel_Temp() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    int cm1 = readUltrasonicDistance(A4, A5) / 29 / 2;  //sensor 1 
    waterLevel1 = maxHeight - cm1;

    int cm2 = readUltrasonicDistance(A3, A2) / 29 / 2;  // sensor 2
    waterLevel2 = maxHeight - cm2;
    // waterLevel2 = maxHeight - cm1;

    int Temp = readTemperature();

    if (waterLevel2 < minHeight) {
      waterLevel2 = minHeight;
    }
    if (waterLevel2 > maxHeight) {
      waterLevel2 = maxHeight;
    }

    if (waterLevel1 < minHeight) {
      waterLevel1 = minHeight;
    }
    if (waterLevel1 > maxHeight) {
      waterLevel1 = maxHeight;
    }

    if (waterLevel2 < setWater2) {
      digitalWrite(A1, HIGH);
    } else {
      digitalWrite(A1, LOW);  
    }
    
    if (waterLevel1 < setWater1) {
      digitalWrite(A1, HIGH);
    } else {
      digitalWrite(A1, LOW);  
    }

    Serial.print(waterLevel1);
    Serial.print(",");
    Serial.print(waterLevel2);
    Serial.print(",");
    Serial.print(nhietdo);
    Serial.println();

    // Send to ESP
    dataSend = dataSend + waterLevel1 + "," + waterLevel2 + "," + nhietdo + "\n";
    mySerial.println(dataSend);
    mySerial.flush();
    dataSend = "";
  }
}

void onServo() {

  unsigned long startTime = millis();    
  unsigned long startTime_2 = millis();  
  unsigned long startTime_3 = millis();  
  unsigned long startTime_4 = millis();  


  digitalWrite(3, HIGH);

  while (millis() - startTime < 30000) {
  }

  digitalWrite(3, LOW);

  while (millis() - startTime < 35000) {
  }
  digitalWrite(12, LOW);  
  tone(13, 12500, 2000);  
  delay(10000);

  while (millis() - startTime_2 < 45000) {
  }

  digitalWrite(3, HIGH);

  while (millis() - startTime_3 < 50000) {
  }

  digitalWrite(3, LOW);

  while (millis() - startTime_4 < 55000) {
  }

  digitalWrite(12, HIGH);
  tone(13, 12500, 2000);
  delay(2000);
}
void onServoLeft() {
  digitalWrite(12, HIGH);
  tone(13, 12500, 2000);
  delay(1000);
}
void onServoRight() {
  digitalWrite(12, LOW);  
  tone(13, 12500, 2000);  
  delay(1000);
}