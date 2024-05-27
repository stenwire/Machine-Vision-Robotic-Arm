#include <Servo.h> 

Servo myservo0;
Servo myservo1;

  //Create a gas pump and solenoid valve control object (Servo myservo0) for the air pump ( Servo myservo1) for the solenoid valve
  // This variable uses the air pump solenoid valve switch (0 is off, 180 is on)

void setup() 
{ 
  myservo0.attach(1);
  myservo1.attach(0);

  myservo0.write(0);  
  myservo1.write(0);  

// Representing the air pump plug 9 pin, the solenoid valve plug 8 pin arduino control
} 

void loop() 
{ 

  myservo0.write(180);   
  myservo1.write(0);

//This line of code indicates that the air pump is on and the solenoid valve is off.
  delay(15000);       
// Indicates that the action time of this group is 1500 milliseconds, and the time can be freely modified.

  myservo0.write(0);   
  myservo1.write(0);

// This line of code indicates that the air pump is off, the solenoid valve is off, and the air pump has moved the item. At this time, the air pump can also be turned on or off according to actual needs.
  delay(800);         
// Wait for 800 milliseconds to get the item to the specified location, the time can be freely modified

  myservo0.write(0);   
  myservo1.write(180);

// This line of code indicates that the air pump is off, the solenoid valve is open, and the item is off the suction cup.
  delay(800);      
//Put down the item waiting time of 800 milliseconds, the time can be freely modified

  myservo0.write(0);   
  myservo1.write(0);

// This line of code indicates that the air pump is off, the solenoid valve is off, and the operation is complete. delay(1500); 
delay(15000);          
// Wait for 1500 milliseconds to cycle. Time can be freely modified. If you don't need to wait for a loop, you can add the number to the super, that is, let him wait indefinitely. Don't let the loop have other code. Unfortunately, I still haven't figured it out. I understand the changes later.

//The last match can't be lost, otherwise all errors
}