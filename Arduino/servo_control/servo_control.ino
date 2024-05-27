#include <Servo.h>

// Define servo objects for three servos
Servo servo1;
Servo servo2;
Servo servo3;

// Function to initialize servos
void initializeServos() {
  servo1.attach(4);  // Attach servo 1 to pin 9
  servo2.attach(5); // Attach servo 2 to pin 10
  servo3.attach(6); // Attach servo 3 to pin 11
}

// Function to move servo 1 to a specified angle
void moveServo1(int angle) {
  servo1.write(angle);
}

// Function to move servo 2 to a specified angle
void moveServo2(int angle) {
  servo2.write(angle);
}

// Function to move servo 3 to a specified angle
void moveServo3(int angle) {
  servo3.write(angle);
}

void setup() {
  // Initialize servos
  initializeServos();
}

void goToStartPos() {
  // Move servo 1 to 0 degrees
  moveServo1(23);
  delay(1000); // Delay for 1 second

  // Move servo 2 to 90 degrees
  moveServo2(180);
  delay(1000); // Delay for 1 second

  // Move servo 3 to 180 degrees
  moveServo3(180);
  delay(1000); // Delay for 1 second
}

void pickUpCube() {
  // Move servo 1 to 0 degrees
  moveServo1(100);
  delay(1000); // Delay for 1 second

  // Move servo 2 to 90 degrees
  moveServo2(100);
  delay(1000); // Delay for 1 second

  // Move servo 3 to 180 degrees
  moveServo3(40);
  delay(1000); // Delay for 1 second
}

void dropCube() {
  // Move servo 1 to 0 degrees
  moveServo1(50);
  delay(1000); // Delay for 1 second

  // Move servo 2 to 90 degrees
  moveServo2(90);
  delay(1000); // Delay for 1 second

  // Move servo 3 to 180 degrees
  moveServo3(180);
  delay(1000); // Delay for 1 second
}

void loop() {
  goToStartPos();
  delay(1000);
  pickUpCube();
  delay(1000);
  // dropCube();
  // delay(1000);

}
