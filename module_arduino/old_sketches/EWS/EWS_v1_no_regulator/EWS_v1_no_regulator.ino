const int motorPin = 2;

// Comments are for attaching the depth regulators
// const int depthRegulatorPin = 3;


void setup() {
  pinMode(motorPin, OUTPUT);
  Serial.println(9600);
  // pinMode(depthRegulatorPin, OUTPUT);
  delay(3000);
}

void loop() {
  digitalWrite(motorPin, HIGH);
  delay(2000);
  digitalWrite(motorPin, LOW);
  delay(2000);
}
