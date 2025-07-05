#ifndef TUTEBY_STEPPER_H
#define TUTEBY_STEPPER_H

#include <Stepper.h>
#include <stdint.h>
#include <Arduino.h>

// Enum for motor speed levels
typedef enum {
    SLOW = 1,  // Slow speed
    MID,        // Medium speed
    FAST        // Fast speed
} SPEED_OF_MOTOR_T;

class TUTEBY_STEPPER {
  private:
    Stepper _stepper_instance; // AccelStepper instance
    uint8_t _is_holding:1;
    uint8_t _pin1;                  // Pin 1 for stepper motor
    uint8_t _pin2;                  // Pin 2 for stepper motor
    uint8_t _pin3;                  // Pin 3 for stepper motor
    uint8_t _pin4;                  // Pin 4 for stepper motor
    float _degree;                  // Step angle of the motor
    long _home_pos;                 // Home position (long for larger values)
    uint16_t _stepsPerRevolution ; 
    SPEED_OF_MOTOR_T speed_t;       // Motor speed type (private for encapsulation)

  public:
    // Constructor to initialize stepper with pins and step angle
    TUTEBY_STEPPER(uint16_t steps ,uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4,uint8_t is_holding = 0);

    // Function to put the motor into an idle state (disable outputs)
    void IdleState(void);

    // Function to initialize motor settings based on speed level
    void init(SPEED_OF_MOTOR_T pdata);

    // Function to set the motor's acceleration
    void SetAcceleration(float speed);

    // Function to set the motor's maximum speed
    void SetMaxAcceleration(float speed);

    // Function to set the motor's speed
    void SetSpeed(long speed);

    // Function to set the motor's home position
    void SetHomePos(long pos);

    // Function to get the motor's current position
    void GetHomePos(long *pos);

    // Function to rotate the motor one full revolution
    void RotateOneRevolution(void);

    // Function to rotate the motor by a specific angle
    void RotateAngle(float degree);

    // Function to rotate the motor by multiple revolutions
    int16_t RotateMultiRevolution(int16_t NumberOfRotation);
    
    // Function to rotate the motor by multiple revolutions Override
    int16_t RotateMultiRevolution(const char* NumberOfRotation);

    // Function to rotate the motor by multiple revolutions Override
    int16_t RotateMultiRevolution(String NumberOfRotation);
};

#endif
