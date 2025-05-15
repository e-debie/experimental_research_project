#include <Adafruit_BME280.h> // loads the Adafruit BME280 library and required I2C
#include <LiquidCrystal.h>

const int rs = 4, en = 3, d4 = 5, d5 = 6, d6 = 7, d7 = 9;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

Adafruit_BME280 bme; // I2C ; // Redefine sensor name to bme in this sketch

const int trigPin = 11;
const int echoPin = 10;
const unsigned int delayT = 1000; // Variable for time between readings

float lastT; // We will store the last recorded data
float soundSpeed;
float duration, distance;
int status;


void sensor_connect() {
  while (!Serial); // This will freeze execution here until
    // Serial returns 0, this indicates a
    // Serial connection is succesfully made .
    // Below we start the BME sensor . Two things happen :
    // - We call bme.begin (), the value 0 x76 indicates
    // the address of the BME on the I2C interface .
    // The default address is 0x76, but 0x77 is the
    // alternative address, enabled by soldering a jumper on
    // the board.
    // - bme.begin() will return a non-zero value if some error
    // occurred. We store this value .

    status = bme.begin(0x76);
    if (! status ){ // If the status is non-zero , we output an error messge
      Serial.print (F(" Could not find a valid BME280 sensor , "));
      Serial.print(F(" check wiring ! Error : "));
      Serial.println(status);
      while (1); // This will freeze execution at this point . If
      // the sensor did not load succesfully , we don’t
      // want to execute the rest of the code
    }
  // If we reach this point of the code , we have succesfully connected
  // to the sensor , so we can display this using the Serial interface .
  Serial.println(F(" Succesfully connected to BME280 sensor ."));
}

void distance_measure() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH) / 1e6;  // convert from us to s
  distance = (duration * soundSpeed) / 2;  // m
  Serial.print("Distance: ");
  Serial.println(distance);
}

void setup() {
  Serial.begin(9600);
  sensor_connect();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.begin(4, 3);

  lcd.print("Distance");
}

void loop() {
  lastT = bme.readTemperature();
  soundSpeed = 331.*sqrt((lastT+273.15)/273.);

  distance_measure();

  lcd.setCursor(0, 1);
  lcd.print(distance);

  delay(delayT);
}