#include <Stepper.h>
#include <Servo.h>

// Stepper motor setup
const int stepsPerRevolution = 200;  // Change this to fit your stepper motor
Stepper motor1(stepsPerRevolution, 8, 9, 10, 11);  // Motor 1 on pins 8-11


// Servo motor setup
Servo myServo;
int servoPin = 6;  // Pin where the servo is connected

void setup() {
  // Initialize stepper motor
  motor1.setSpeed(150);

  // Initialize servo motor
  myServo.attach(servoPin);

  // Initialize serial communication
  Serial.begin(9600);
  Serial.println("Commands:");
  Serial.println("'o' -> Move the servo to 70 degrees.");
  Serial.println("'s' -> Move the servo to 0 degrees.");
  Serial.println("Numeric input -> Move the stepper motor that many steps.");
}

void loop() {
  if (Serial.available() > 0) {
    // Read the input string
    String input = Serial.readStringUntil('\n');
    input.trim();  // Remove extra spaces and newline characters

    // Check if the input is "o" (case insensitive)
    if (input.equalsIgnoreCase("o")) {
      myServo.write(150);  // Move the servo to 70 degrees
      Serial.println("Servo motor: Moved to 70 degrees.");
    } 
    // Check if the input is "s" (case insensitive)
    else if (input.equalsIgnoreCase("s")) {
      myServo.write(0);  // Move the servo to 0 degrees
      Serial.println("Servo motor: Moved to 0 degrees.");
    }
    // Check if the input is numeric for the stepper motor
    else if (isNumeric(input)) {
      int stepsToMove = input.toInt();  // Convert to integer
      Serial.print("Stepper motor: Moving ");
      Serial.print(stepsToMove);
      Serial.println(" steps.");
      motor1.step(stepsToMove);
      digitalWrite(8,0);
      digitalWrite(11,0);

      Serial.println("Stepper motor movement complete.");
    } 
    // Handle invalid input
    else {
      Serial.println("Invalid input. Use 'o', 's', or a number.");
    }
  }
}

// Helper function to check if a string is numeric
bool isNumeric(String str) {
  for (unsigned int i = 0; i < str.length(); i++) {
    if (!isDigit(str[i]) && str[i] != '-') {
      return false;
    }
  }
  return true;
}
