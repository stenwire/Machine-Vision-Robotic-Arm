#include <Servo.h>

#define NUM_SERVOS 4
Servo servos[NUM_SERVOS];

int pinServo1 = 2;
int pinServo2 = 3;
int pinServo3 = 4;
int pinServo4 = 5;

int suctionMotor = 6;
int suctionState = LOW; // Initialize suction state to off

int initialPos[4] = {20, 40, 60, 80};
int dropRedPos[4] = {20, 40, 60, 80};

void setServoPosition(Servo servo, int angle) {
  // Set servo position
  servo.write(angle);
  delay(1000); // Delay for smoother movement, adjust as needed
}

void goToStartPosition() {
  // Move arm to initial position
  // sequence of movement:
    // move shoulder
    // move elbow
    // move wrist
    // move base

  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], initialPos[i]);
  }
}

void setupServos() {
  // Attach servos to pins
  servos[0].attach(9);  // Base
  servos[1].attach(10); // Shoulder
  servos[2].attach(11); // Elbow
  servos[3].attach(12); // Wrist
}

void setup() {
  pinMode(suctionMotor, OUTPUT); // Set suction motor pin as output
  Serial.begin(115200);
  setupServos();
}

void loop() {
  goToStartPosition();
  if (Serial.available() > 0) {
    Serial.println("======== Connection to raspberryPI established ======");
    String angles = Serial.readStringUntil('\n');
    Serial.print("Angles: ");
    Serial.println(angles);
    moveArmToRedBox(angles);
    delay(2000); // Delay for demonstration purposes
    dropRedBox();
    delay(2000); // Delay for demonstration purposes
    // Add logic to send end programif no box is detected after 60 seconds
  }
}

void moveArmToRedBox(String angles) {
  // sequence of movement:
    // move base
    // move elbow
    // move shoulder
    // no need to move wrist

  // Parse the received string
  int servoAngles[NUM_SERVOS];
  int index = 0;
  int prevIndex = 0;

  // Populate servo angles from serial
  for (int i = 0; i < angles.length(); i++) {
    if (angles.charAt(i) == ',' || angles.charAt(i) == '\n') {
      servoAngles[index] = angles.substring(prevIndex, i).toInt();
      index++;
      prevIndex = i + 1;
    }
  }

  // Set servo positions from angles
  moveBase(servoAngles[0]);
  moveShoulder(servoAngles[1]);
  moveElbow(servoAngles[2]);

  // Activate suction cup
  delay(2000);
  sunctionCup(1);

}

void moveBase(int servoAngle) {
  int og_position = initialPos[0];
  if (servoAngle < og_position || servoAngle > 180) {
    Serial.println("Object out of reach");
    return;
  }
  for (int pos = og_position; pos <= servoAngle; pos += 1) {
    servos[0].write(pos);
    delay(15); // wait 15 milliseconds for the servo to reach the position
  }
}

void moveShoulder(int servoAngle) {
  int og_position = initialPos[1];
  if (servoAngle < og_position || servoAngle > 180) {
    Serial.println("Object out of reach");
    return;
  }
  for (int pos = og_position; pos <= servoAngle; pos += 1) {
    servos[1].write(pos);
    delay(15); // wait 15 milliseconds for the servo to reach the position
  }
}

void moveElbow(int servoAngle) {
  int og_position = initialPos[2];
  if (servoAngle < og_position  || servoAngle > 180) {
    Serial.println("Object out of reach");
    return;
  }
  for (int pos = og_position; pos <= servoAngle; pos += 1) {
    servos[2].write(pos);
    delay(15); // wait 15 milliseconds for the servo to reach the position
  }
}

void sunctionCup(int state) {
  // Activate/deactivate suction cup
  if (state == 1) {
    digitalWrite(suctionMotor, HIGH);
    Serial.println("Suction cup activated");
  } else if (state == 0) {
    digitalWrite(suctionMotor, LOW);
    Serial.println("Suction cup deactivated");
  } else {
    Serial.println("Error operating suction cup");
  }
}

void dropRedBox() {
  // Move arm to position for dropping red box
  for (int i = 0; i < 4; i++) {
    setServoPosition(servos[i], dropRedPos[i]);
  }
  delay(2000);
  // Deactivate suction cup
  sunctionCup(0);
}
