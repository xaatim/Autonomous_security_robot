#include <Wire.h>
#include <Adafruit_INA219.h>


int ENA = 3;
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;
int ENB = 9;
int trigPin = 11;
int echoPin = 10;
int redLedPin = 6;
int greenLedPin = 4;

float Soc;
float minVolt = 9;
float maxVolt = 12.6;
float distance;
float busvoltage = 0;
float speedOfSound = 0.343;  //speed of sound in (mm/µs)
float pingTravelTime;

Adafruit_INA219 ina219;


void setup() {

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLedPin, OUTPUT);
  

  Serial.begin(115200);
  while (!Serial) {

    delay(1);
  }

  if (!ina219.begin()) {
    while (1) { delay(10); }
  }
}

void actions(bool con1, bool con2, bool con3, bool con4, int delay_in_ms = 3000) {
  analogWrite(ENA, 255);
  analogWrite(ENB, 255);

  digitalWrite(IN1, con1);
  digitalWrite(IN2, con2);
  digitalWrite(IN3, con3);
  digitalWrite(IN4, con4);
}

float get_distance(float delay_time = 10) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(delay_time);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(delay_time);
  digitalWrite(trigPin, LOW);
  pingTravelTime = pulseIn(echoPin, HIGH);  // in micro seconds
  delay(100);
  return speedOfSound * pingTravelTime / 2;
}

void loop() {

  Soc = ((ina219.getBusVoltage_V() - minVolt) / (maxVolt - minVolt)) * 100;
  distance = get_distance();
  // ledDebug(distance);
  Serial.print(Soc);
  Serial.print(",");
  Serial.println(distance);
  if (Serial.available()>0){
    char keys = Serial.read();

  if (keys == 'f' || keys == 'F') {
    actions(true, false, false, true);  // Forward
  } else if (keys == 'b' || keys == 'B') {
    actions(false, true, true, false);  // Backward
  } else if (keys == 'r' || keys == 'R') {
    actions(true, false, true, false);  // Right
  } else if (keys == 'l' || keys == 'L') {
    actions(false, true, false, true);  // Left
  } else if (keys == 'q' || keys == 'Q') {
    actions(false, false, false, false);  // Stop
  }

  }


  
}

void ledDebug(float distance) {
  if (distance >= 100) {
    digitalWrite(greenLedPin, HIGH);

  } else if (distance <= 100) {
    Serial.println("distance is less than 10cm");
    digitalWrite(greenLedPin, LOW);
    digitalWrite(redLedPin, HIGH);
    digitalWrite(redLedPin, LOW);
  }
}

void moveRobot(bool con1, bool con2, bool con3, bool con4) {
  int speed = 70;
  analogWrite(enA, speed);
  analogWrite(enB, speed);

  digitalWrite(in1, con1);
  digitalWrite(in2, con2);

  digitalWrite(in3, con3);
  digitalWrite(in4, con4);

  // moveRobot(LOW, HIGH, LOW, HIGH);  // forward
  // moveRobot(HIGH, LOW, HIGH, LOW);  // backward
  // moveRobot(LOW, HIGH, HIGH, LOW);  // right 
  // moveRobot(HIGH, LOW, LOW, HIGH);  // Left
}231