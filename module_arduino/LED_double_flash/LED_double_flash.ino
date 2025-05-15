const int DELAY = 500; // Delay in ms
const int PIN_AMOUNT = 4;
int LEDS[PIN_AMOUNT] = { 2, 3, 4, LED_BUILTIN };
bool statuses[PIN_AMOUNT] = { true, false, true, false };

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i<PIN_AMOUNT; i++) {
    pinMode(LEDS[i], OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i<PIN_AMOUNT; i++) {
    digitalWrite(LEDS[i], statuses[i]);
    statuses[i] = not statuses[i];
  }
  delay(DELAY);
}
