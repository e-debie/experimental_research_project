/*
* The circuit :
* SD card attached to SPI bus as follows :
MOSI - pin 11 |
MISO - pin 12 | These pins are connected to the hardware SPI -bus
CLK - pin 13 |
CS - pin 10 - Chip Select pin can be chosen freely ; default is pin 10
See https://www.arduino.cc/en/reference/board
*/
#include <SPI.h>
#include <SD.h>
#include <Adafruit_BME280.h> // loads the Adafruit BME280 library and required I2C
#include "RTClib.h"

RTC_DS3231 rtc;

Adafruit_BME280 bme; // I2C ; // Redefine sensor name to bme in this sketch
unsigned int delayT = 5000; // Variable for time between readings
float lastT , lastP , lastH ; // We will store the last recorded data

// "const" means constant: this value will not change while running
// This will allow the compiler to optimize
const int csPin = 10;
String FileName = "DATA.TXT";

File myFile;
String lastOutput;
int status;
String lastTime;

void RC_connect() {
  Serial.println("Connecting to RTC");
  if (!rtc.begin()) {
    Serial.println("Couldn’t find RTC");
    Serial.flush();
    while (1) delay(10);
  }
  if (rtc.lostPower()) {
    // When time needs to be set on a new device, or after a power loss, the
    // following lines sets the RTC to the date & time from the user input through Serial
    Serial.println("RTC lost power! Please enter the current date and time in format YYYY MM DD HH MM SS:");
    while (!Serial.available());
    int year, month, day, hour, minute, second;
    while (Serial.available() < 19); // Wait for full input
    year = Serial.parseInt();
    month = Serial.parseInt();
    day = Serial.parseInt();
    hour = Serial.parseInt();
    minute = Serial.parseInt();
    second = Serial.parseInt();
    rtc.adjust(DateTime(year, month, day, hour, minute, second));
    Serial.println("RTC time set successfully.");
  }
  Serial.println("RTC connected successfully");
}


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
      Serial.print (" Could not find a valid BME280 sensor , ");
      Serial.print(" check wiring ! Error : ");
      Serial.println(status);
      while (1); // This will freeze execution at this point . If
      // the sensor did not load succesfully , we don’t
      // want to execute the rest of the code
    }
  // If we reach this point of the code , we have succesfully connected
  // to the sensor , so we can display this using the Serial interface .
  Serial.println(" Succesfully connected to BME280 sensor .");
}

void sd_connect() {
  // Open serial communications and wait for port to open :
  Serial.println(" Initializing SD card ... ");
  if (!SD.begin(csPin)) {
    Serial.println(" initialization failed !");
    return;
  }
  Serial.println(" initialization done .");
}

void sd_writeln(String line) {
  // Open the file for writing
  myFile = SD.open(FileName, FILE_WRITE);
  // If the file opened all right , write to it:
  if (myFile) {
    Serial.println("Writing to " + FileName);
    myFile.println(line);
    // close the file
    myFile.close();
    Serial.println(" Writing to file done !");
  } else {
    // if the file didn ’t open , print an error message :
    Serial.println(" error opening file for writing ");
  }
  myFile.close();
}

String RC_read() {
  DateTime now = rtc.now();
  int year = now.year() ;
  int month = now.month();
  int day = now.day();
  int hour = now.hour();
  int minute = now.minute();
  int second = now.second();
  char time[30];  
  snprintf(time, sizeof(time), "%04d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, minute, second);
  String output = String(now.unixtime()) + "\t" + String(time);
  return output;
}

void sd_read() {
  // Re - open the file for reading :
  myFile = SD.open(FileName);
  if (myFile) {
    Serial.println(" Data in file " + FileName);
    // read from the file until there ’s nothing else in it:
    while (myFile.available()) {
      Serial.write(myFile.read());
    }
    // close the file :
    myFile.close();
    while (1) {}
  } else {
    // if the file didn ’t open , print an error message :
    Serial.println(" error opening file for reading ");
  }
}

void display_freeram() {
  Serial.print(F("- SRAM left: "));
  Serial.println(freeRam());
}

int freeRam() {
  extern int __heap_start,*__brkval;
  int v;
  return (int)&v - (__brkval == 0  
    ? (int)&__heap_start : (int) __brkval);  
}

void setup() {
  Serial.begin(9600);
  RC_connect();
  sensor_connect();
  sd_connect();

  // We delete and recreate the file to clear its content
  int rem = SD.remove(FileName);
  Serial.print(" removing file, status : ");
  Serial.println(rem);
  myFile = SD.open(FileName, FILE_WRITE);
  myFile.println("# t (UNIX)\tt (ISO 8601)\tT (C)\tRH (%)");
  myFile.close();
}


void loop() {
  lastT = bme.readTemperature(); // Temperature
  lastP = bme.readPressure(); // Pressure
  lastH = bme.readHumidity(); // Relative Humidity
  
  // lastTime = RC_read();

  lastOutput = String(lastT) + "\t" + String(lastP) + "\t" + String(lastH);
  sd_writeln(lastOutput);

  delay(delayT);

  display_freeram();
}