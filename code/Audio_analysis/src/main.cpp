#include <Audio.h>

#define MICROPHONE_PIN A1

const int buttonPin = 2;
const int led_pin = 3;  // LED pin
bool speakerOn = false;

// Audio objects
AudioSynthWaveformSine sineWave;
AudioOutputAnalog dacOutput;
AudioConnection patchCord(sineWave, dacOutput);

const int sampleWindow = 50; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;

unsigned long startAudioMillis = 0; // Start of sample window
unsigned int count = 0; // Counter for the number of samples

bool buttonState = false; // Variable to store the button state

void setup() {
    pinMode(buttonPin, INPUT_PULLUP);  // Internal pull-up resistor
    AudioMemory(10);

    sineWave.frequency(100);  // 440 Hz (A4 note)
    sineWave.amplitude(0);  // Start muted

    Serial.begin(115200);
    pinMode(MICROPHONE_PIN, INPUT);
    analogReadResolution(10);
    Serial.println("Microphone connected to pin A1");

    digitalWrite(LED_BUILTIN, HIGH);  // Set button pin HIGH
    delay(1000);  // Wait for a second
    digitalWrite(LED_BUILTIN, LOW);  // Set button pin LOW

    startAudioMillis = millis();  // Start the audio sample window
    sineWave.amplitude(0.1);  // Set amplitude to 0.5

    pinMode(buttonPin, INPUT_PULLUP);  // Set button pin as input with pull-up resistor
}

void loop() {
    digitalWrite(led_pin, buttonState ? HIGH : LOW);  // Set LED state based on button state

    if (digitalRead(buttonPin) == LOW) {  // Button pressed
        buttonState = !buttonState;  // Toggle button state
        if (buttonState) {
            sineWave.amplitude(0);  // Set amplitude to 0.5
        } else {
            sineWave.amplitude(0);  // Mute the speaker
        }
    }

    unsigned long startMillis= millis();  // Start of sample window
    unsigned int peakToPeak = 0;   // peak-to-peak level

    unsigned int signalMax = 0;
    unsigned int signalMin = 1024;

    // collect data for 50 mS
    while (millis() - startMillis < sampleWindow)
    {
        sample = analogRead(MICROPHONE_PIN);
        if (sample < 1024)  // toss out spurious readings
        {
            if (sample > signalMax)
            {
                signalMax = sample;  // save just the max levels
            }
            else if (sample < signalMin)
            {
                signalMin = sample;  // save just the min levels
            }
        }
    }
    peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude

    // write the value peakToPeak in a CSV file
    

    Serial.println(peakToPeak);

    if (millis() - startAudioMillis > 2000) {
        count++;
        sineWave.frequency(100 + count * 50);  // Increase frequency by 50 Hz every second
        startAudioMillis = millis();  // Reset the start time
    }
}