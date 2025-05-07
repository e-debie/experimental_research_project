const int OUT_PORT = 2; // Port on which the LED is connected
const int DELAY = 100; // Delay in ms

void setup() {
  // put your setup code here, to run once:
  pinMode(OUT_PORT, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(OUT_PORT, HIGH);

}
