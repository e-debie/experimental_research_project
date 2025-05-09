/*
 * HC-SR04 example sketch
 *
 *   VCC -> 5V
 *   GND -> GND
 *   Trig -> Pin 9 
 *   Echo -> Pin 10
 */

const int trigPin = 9;
const int echoPin = 10;

float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH) / 1e6;  // convert from us to s
  distance = (duration * speed_sound) / 2;  // m
  Serial.print("Distance: ");
  Serial.println(distance);
  delay(100);
}