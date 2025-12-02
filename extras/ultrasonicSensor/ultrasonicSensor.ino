int trigPin = 12;
int echoPin = 11;
int greenLedPin = 4;
int redLedPin = 6;
int distance;
int pingTravelTime;
float speedOfSound = 0.343;  //speed of sound in (mm/µs)

void setup() {
  // put your setup code here, to run once:
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLedPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  pingTravelTime = pulseIn(echoPin, HIGH);  // in micro seconds
  distance = speedOfSound * pingTravelTime / 2;
  Serial.println("distance: " + String(distance));
  Serial.println("time: " + String(pingTravelTime));
  Serial.println();
  delay(100);
  if (distance >= 100) {
    digitalWrite(greenLedPin, HIGH);

  } else if (distance <= 100) {
    Serial.println("distance is less than 10cm");
    digitalWrite(greenLedPin, LOW);
    digitalWrite(redLedPin, HIGH);
    delay(20);
    digitalWrite(redLedPin, LOW);
    
  }
  delay(100);
}
