// Panic Button - ESP32 side
// Wiring: one leg of the button -> GPIO 4, other leg -> GND
// (internal pull-up is used, so no resistor needed)

const int BUTTON_PIN = 14;
const unsigned long DEBOUNCE_MS = 50;

int lastReading = HIGH;
int stableState = HIGH;
unsigned long lastChange = 0;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int reading = digitalRead(BUTTON_PIN);

  if (reading != lastReading) {
    lastChange = millis();
    lastReading = reading;
  }

  if (millis() - lastChange > DEBOUNCE_MS && reading != stableState) {
    stableState = reading;
    if (stableState == LOW) {      // button pressed
      Serial.println("PANIC");
    }
  }
}
