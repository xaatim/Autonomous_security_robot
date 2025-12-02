String keys;

int output1 = 2;
int output2 = 3;
int output3 = 12;
int output4 = 11;

int ENA = 9;   // Left motor enable
int ENB = 10;  // Right motor enable

int current_speed = 0;
int target_speed = 0;
int max_speed = 255;
int accel_step = 15;   // speed increase per step
unsigned long last_update = 0;
int accel_interval = 100; // ms

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  pinMode(output1, OUTPUT);
  pinMode(output2, OUTPUT);
  pinMode(output3, OUTPUT);
  pinMode(output4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
}

void driveMotors(int direction) {
  if (direction == 1) {         // forward
    digitalWrite(output1, true);
    digitalWrite(output2, false);
    digitalWrite(output3, false);
    digitalWrite(output4, true);
  } else if (direction == -1) { // backward
    digitalWrite(output1, false);
    digitalWrite(output2, true);
    digitalWrite(output3, true);
    digitalWrite(output4, false);
  } else if (direction == 2) {  // right
    digitalWrite(output1, true);
    digitalWrite(output2, false);
    digitalWrite(output3, true);
    digitalWrite(output4, false);
  } else if (direction == -2) { // left
    digitalWrite(output1, false);
    digitalWrite(output2, true);
    digitalWrite(output3, false);
    digitalWrite(output4, true);
  } else {                      // stop
    digitalWrite(output1, false);
    digitalWrite(output2, false);
    digitalWrite(output3, false);
    digitalWrite(output4, false);
  }
}

void updateSpeed() {
  unsigned long now = millis();
  if (now - last_update >= accel_interval) {
    if (current_speed < target_speed) current_speed += accel_step;
    else if (current_speed > target_speed) current_speed -= accel_step;

    if (current_speed > max_speed) current_speed = max_speed;
    if (current_speed < -max_speed) current_speed = -max_speed;

    int pwm = abs(current_speed);
    analogWrite(ENA, pwm);
    analogWrite(ENB, pwm);

    last_update = now;
  }
}

void loop() {
  if (Serial.available() > 0) {
    char key = Serial.read();

    if (key == 'f' || key == 'F') {
      target_speed = max_speed;
      driveMotors(1);
    } else if (key == 'b' || key == 'B') {
      target_speed = max_speed;
      driveMotors(-1);
    } else if (key == 'r' || key == 'R') {
      target_speed = max_speed;
      driveMotors(2);
    } else if (key == 'l' || key == 'L') {
      target_speed = max_speed;
      driveMotors(-2);
    } else if (key == 'q' || key == 'Q') {
      target_speed = 0;
      driveMotors(0);
    }
  }

  updateSpeed(); // smooth acceleration
}
