// Final Year Project

#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int pinServo1 = 2;
int pinServo2 = 3;
int pinServo3 = 4;
int pinServo4 = 5;

int sunctionMotor = 2;
int sunctionState[2] = {0,1};

int initialPos[4] = {20, 40, 60, 80};
int dropRedPos[4] = {20, 40, 60, 80};
int dropBluePos[4] = {20, 40, 60, 80};
int dropGreenPos[4] = {20, 40, 60, 80};

Servo servos[4] = {servo1, servo2, servo3, servo4};

void setup() {
  // put your setup code here, to run once:
  servo1.attach(pinServo1);
  servo2.attach(pinServo2);
  servo3.attach(pinServo3);
  servo4.attach(pinServo4);

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

}


void moveArmToObject() {}


void sunctionCup(int position) {
  if (position == 1) {
    digitalWrite(sunctionMotor, HIGH);
  } else {
    digitalWrite(sunctionMotor, LOW);
  }
}


void goToStartPosition() {
  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], initialPos[i]);
    delay(1000);
  }
}


void setServoPosition(Servo servo, int angle) {
  servo.write(angle);
  delay(1000);
}


void dropRed() {
  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], dropRedPos[i]);
    delay(1000);
  }
  sunctionCup(0);
}


void dropBlue() {
  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], dropBluePos[i]);
    delay(1000);
  }
  sunctionCup(0);
}


void dropGreen() {
  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], dropGreenPos[i]);
    delay(1000);
  }
  sunctionCup(0);
}



