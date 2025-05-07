/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://docs.arduino.cc/hardware/

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://docs.arduino.cc/built-in-examples/basics/Blink/
*/

const int DELAY = 10000; // Delay between blinks in ms
int current_number;
bool current_prime;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  if (Serial.available() > 0) {
    current_number = Serial.parseInt();
    current_prime = check_prime(current_number); // Determines whether the input number is prime
    digitalWrite(LED_BUILTIN, current_prime); // HIGH is the same as true, and LOW is the same as false. Hence, we can simply parse the 'primeness' of the number to the light.
    Serial.print("Value " + String(current_number) + " is ");
    if (not current_prime) Serial.print("not ");
    Serial.println("prime.");
  }
}

bool check_prime(int inps) {
  bool is_prime = true;
  for (int i = 2; i<=inps/2; i++) {
    // inps/i is going to be a whole number if inps is divisible by i (and therefore not prime). In that case, (inps/i)*i will equal inps.
    // If inps is not divisible by i, then inps/i will instead be truncated (in this case, rounded down). Then, (inps/i)*i will not equal inps (as floor(inps/i)*i != inps).
    if ((inps/i)*i == inps) { 
      is_prime = false;
      break;
    }
  }
  return is_prime;
}