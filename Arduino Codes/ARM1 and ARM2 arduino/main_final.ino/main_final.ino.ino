#include <Arduino.h>
#include "tuteby_stepper.h"

// Prototype uint16_t steps ,uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4, uint8_t is_holding=0 //default false
TUTEBY_STEPPER stepper1(200, 8, 9, 10, 11, 1);
TUTEBY_STEPPER stepper2(200, 4, 5, 6, 7, 1);
bool isNumeric(String str);
void setup()
{
  stepper1.init(MID);
  stepper2.init(MID);
  // stepper1.RotateMultiRevolution(400);
  Serial.begin(9600);
  Serial.println("Enter steps for both motors in format: <steps_motor1>,<steps_motor2>");
  stepper1.RotateMultiRevolution(100);
  stepper2.RotateMultiRevolution(100);
}

void loop()
{
  if (Serial.available() > 0)
  {
    // Read the input string:
    String input = Serial.readStringUntil('\n');
    input.trim(); // Remove extra spaces or newline characters

    // Split input into two parts based on the comma:
    int commaIndex = input.indexOf(',');
    if (commaIndex == -1)
    {
      Serial.println("Invalid input. Enter in format: <steps_motor1>,<steps_motor2>");
      return;
    }
    String motor1StepsStr = input.substring(0, commaIndex);
    String motor2StepsStr = input.substring(commaIndex + 1);

    if (!isNumeric(motor1StepsStr) || !isNumeric(motor2StepsStr))
    {
      Serial.println("Invalid input. Steps must be integers.");
      return;
    }

    // int motor1Steps = motor1StepsStr.toInt();
    // int motor2Steps = motor2StepsStr.toInt();
    Serial.print("Motor 1: Moving ");
    Serial.print(motor1StepsStr);
    Serial.println(" steps.");
    Serial.print("Motor 2: Moving ");
    Serial.print(motor2StepsStr);
    Serial.println(" steps.");
    Serial.print("Motor 1: Moved ");
    Serial.println(stepper1.RotateMultiRevolution(motor1StepsStr));
    Serial.print("Motor 2: Moved ");
    Serial.println(stepper2.RotateMultiRevolution(motor2StepsStr));

    Serial.println("Movement complete. Enter next steps:");
  }
}

bool isNumeric(String str)
{
  for (unsigned int i = 0; i < str.length(); i++)
  {
    if (!isDigit(str[i]) && str[i] != '-')
    {
      return false;
    }
  }
  return true;
}