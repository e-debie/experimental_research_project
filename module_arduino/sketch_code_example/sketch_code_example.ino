/*
sketch_code_example
Write here what your code does.
For exmaple, in this sketch, we calculate the table of an integer (7 by default) 10 times,
or until the maximum value is reached (50 by default), after which the code ends in
an infinite empty loop. The output is printed on serial.
The circuit:
- Arduino UNO R3 connected over serial USB
created 10 Mar 2025
for the ERP Arduino module
*/

// Load libraries (often required for specific commands)
#include <SoftwareSerial.h> // Library to use serial input and output

// Define global variables
int INT = 7; // Table of this integer
int MAXVAL = 50; // Integer maximum result of calculation
char TOOHIGH = "Exceeded, quitting... "; // String displayed when max is exceeded
const unsigned long BAUD_RATE = 9600;

// Setup definitions
void setup() {
  // sets the baud rate (bits per second) of data transfer over serial connection to your PC
  Serial.begin(BAUD_RATE);
  
  // Print to Serial Monitor, "..." indicates string
  Serial.print("The table of " + String(INT));
  Serial.print("\n"); // New line character
} // end of setup

void loop() {
  int k; // local v riable
  for (int j = 1; j <= 10; j++) { // for loop with local variable j running from 1 to 10
    k = Mult(INT, j); // user-defined function ( see code at end of sketch )
    if (k < MAXVAL) { // If k does not exceeds the maximum value, give the result
      // prints a line ending with a new line character
      Serial.println(String(j) + " times " + String(INT) + " = " + String(k));
      delay(500); // Pause of 500 ms between each output
      }
    else { // If k exceeds the maximum value, exit the loop
      Serial.println(TOOHIGH);
      break;
    }
  } // end of for loop
  
  while (1) { // This empty while loop will run indefinitely
  }
} // end of main loop


// User-defined functions
/* Our function Mult takes as input two integers and
gives the multiplication of the two as output
*/
int Mult(int x, int y) {
  int result = x * y;
  return result;
}
