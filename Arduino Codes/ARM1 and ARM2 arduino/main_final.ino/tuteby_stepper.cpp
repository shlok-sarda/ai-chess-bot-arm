#include "tuteby_stepper.h"
#include <Stepper.h>
#include <stdint.h>
#include <math.h>
#include <Arduino.h>
/*
Aspect	            setAcceleration()	                                                        setSpeed()
Purpose	            Controls how quickly the motor speeds up or slows down (acceleration).	  Sets a fixed speed for the motor.
Units	              Steps per second squared (steps/second²).	                                Steps per second (steps/second).
Smooth Transitions	Allows gradual ramp-up or ramp-down of speed.	                            No ramp-up; the motor instantly runs at the set speed.
Use Case	          When you need smooth and realistic motion.	                              When you need constant speed immediately.

*/

// Constructor: initializes the pin
TUTEBY_STEPPER::TUTEBY_STEPPER(uint16_t steps ,uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4,uint8_t is_holding = 0)
    :_is_holding(is_holding), _stepsPerRevolution(steps), _pin1(pin1), _pin2(pin2), _pin3(pin3), _pin4(pin4),
      _stepper_instance(steps, pin1, pin2, pin3, pin4)
{
  // _stepper_instance.setCurrentPosition(0); // set position to 0
}

void TUTEBY_STEPPER::IdleState(void) {

  if (_is_holding == 0){
    digitalWrite(_pin1,LOW);
    digitalWrite(_pin2,LOW);
    digitalWrite(_pin3,LOW);
    digitalWrite(_pin4,LOW);
  }else{
    // digitalWrite(_pin1,LOW);
    // digitalWrite(_pin2,LOW);
    digitalWrite(_pin3,LOW);
    digitalWrite(_pin4,LOW);
  }
}

void TUTEBY_STEPPER::SetAcceleration(float speed)
{
  // _stepper_instance.setAcceleration(speed); // Set acceleration
}

void TUTEBY_STEPPER::SetMaxAcceleration(float speed)
{
  // _stepper_instance.setMaxSpeed(speed); // Set acceleration
}

void TUTEBY_STEPPER::SetSpeed(long speed){
  _stepper_instance.setSpeed(speed);
}

void TUTEBY_STEPPER::SetHomePos(long pos){
  // _stepper_instance.setCurrentPosition(pos);
}

void TUTEBY_STEPPER::GetHomePos(long *pos) {
  // *pos = _stepper_instance.currentPosition(); // Set the passed pointer to the current position
  _home_pos = *pos; // Also store it in the private member variable _home_pos
}

void TUTEBY_STEPPER::RotateOneRevolution(){
  // float __revolve_stepper = 360/_degree;
  // _stepper_instance.moveTo(__revolve_stepper);
}

void TUTEBY_STEPPER::RotateAngle(float angle){
  /*
  1 step = 1.8*
  1 deg = 1/1.8*
  60 deg = 60/1.8
  */
  // if (angle < 0) {
  //   angle = 0; // Avoid negative angles
  // }
  // float __new_step = angle / _degree;
  // uint16_t __step = round(__new_step);
  // _stepper_instance.moveTo(__step);
}

int16_t TUTEBY_STEPPER::RotateMultiRevolution(int16_t NumberOfRotation) {
  _stepper_instance.step(NumberOfRotation);
  IdleState();
  return NumberOfRotation;
}

int16_t TUTEBY_STEPPER::RotateMultiRevolution(const char* NumberOfRotation) {
  
  int16_t __NumberOfRotation = atoi(NumberOfRotation);
  _stepper_instance.step(__NumberOfRotation);
  IdleState();
  return __NumberOfRotation;
}

int16_t TUTEBY_STEPPER::RotateMultiRevolution(String NumberOfRotation) {
  
  int16_t __NumberOfRotation = atoi(NumberOfRotation.c_str());
  _stepper_instance.step(__NumberOfRotation);
  IdleState();
  return __NumberOfRotation;
}

void TUTEBY_STEPPER::init(SPEED_OF_MOTOR_T pdata){
  uint16_t __acceleration = 0;
  uint16_t __speed = 0;
  switch (pdata)
  {
  case SLOW:
    __acceleration = 60;
    __speed = 200;
    break;

  case MID:
    __acceleration = 40;
    __speed = 500;
    break;

  case FAST:
    __acceleration = 300;
    __speed = 1000;
    break;
  default:
    break;
  }
  // SetSpeed(__speed);
  SetSpeed(__acceleration);
}
