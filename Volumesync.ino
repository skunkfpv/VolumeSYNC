#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const int potPin = 2;  // Change this to the desired pin for the potentiometer

void drawProgressBar(int percentage) {
  int progressBarWidth = map(percentage, 0, 100, 0, SCREEN_WIDTH);
  display.fillRect(0, SCREEN_HEIGHT - 10, progressBarWidth, 10, SSD1306_WHITE);
}

void setup() {
  Serial.begin(115200);
  
  if (!display.begin(0x3C)) {  // Change 0x3C to the actual I2C address of your OLED display
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  display.display();
  delay(2000);  // Pause for 2 seconds

  // Display "VOLUME SYNC" text for 1 second
  display.clearDisplay();
  display.setTextSize(2); // Change text size here
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("VOLUME");
  display.print("SYNC");
  display.display();
  delay(1000);
}

void loop() {
  int sensorValue = analogRead(potPin);
  int volume = map(sensorValue, 0, 1023, 0, 100);
  
  display.clearDisplay();
  
  // Display volume percentage
  display.setTextSize(5); // Change text size here
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print(volume);
  display.print("%");

  // Draw progress bar
  drawProgressBar(volume);

  // Display additional text below percentage
  display.setTextSize(1); // Adjust text size as needed
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, SCREEN_HEIGHT - 9);  // Adjust Y position to place it just below the percentage
  display.print("@skunkfpv");
  
  display.display();

  Serial.println(volume);
  delay(25);  // Adjust as needed
}
