#include "Ultrasonic.h"
#include <Servo.h>
#include "Timer.h"
Timer timer;

/// communicate with rasp
String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete

Ultrasonic ultrasonic(4);
Servo leftArm;  // create servo object to control a servo
int servo_val; //current servo_angle
int goal_servo_val; //goal servo_angle
int RangeInCentimeters; //distance

void setup() {
  Serial.begin(9600);
  leftArm.attach(9);  // attaches the servo on pin 9 to the servo object
  int ultraEvent = timer.every(50, doUltra, (void*)0); //do function per 1sec
  int motorEvent = timer.every(10, doMotor, (void*)0);
  inputString.reserve(200);
  servo_val = 90;
  goal_servo_val = 90;

}

void loop() {
  timer.update();

  if(Serial.available() >0){
      char inChar = (char)Serial.read();
      // add it to the inputString:
      inputString += inChar;
      // if the incoming character is a newline, set a flag so the main loop can
      // do something about it:
      if (inChar == '*') {
        stringComplete = true;
      }
  }
  
  // print the string when a newline arrives:
  if (stringComplete) {
    int length_str = inputString.indexOf('*');
    if(length_str != -1){
      inputString = inputString.substring(0,length_str);
      //Serial.println(inputString);
      goal_servo_val = inputString.toInt();
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }

  
}

void doMotor(void* context)
{
  if(RangeInCentimeters< 15)
    goal_servo_val = 140 - 6*RangeInCentimeters;
    
  if(servo_val != goal_servo_val)
  {
    if(servo_val > goal_servo_val)
      servo_val--;
    if(servo_val < goal_servo_val)
      servo_val++;
    leftArm.write(servo_val);
  }  
}

void doUltra(void* context)
{
  RangeInCentimeters = ultrasonic.MeasureInCentimeters(); // two measurements should keep an interval
  Serial.print(RangeInCentimeters);//0~400cm
  Serial.print("*");
  Serial.print(goal_servo_val);
  Serial.println("");
}


