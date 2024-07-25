#include <Arduino.h>
#include <IRremote.hpp> // include the library

#define DECODE_NEC // Includes Apple and Onkyo
#define IR_RECEIVE_PIN      2

int buzzer_pin = 6;

void setup() {
    Serial.begin(115200);
    while (!Serial); // Wait for Serial to become available. Is optimized away for some cores.

    // Just to know which program is running on my Arduino
    Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));

    // Start the receiver and if not 3. parameter specified, take LED_BUILTIN pin from the internal boards definition as default feedback LED
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);

    Serial.print(F("Ready to receive IR signals of protocols: "));
    printActiveIRProtocols(&Serial);

    pinMode(buzzer_pin, OUTPUT);
}

void loop() {
    // Check if received data is available and if yes, try to decode it.
    if (IrReceiver.decode()) {
        // Print a summary of received data
        if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
            Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
            // We have an unknown protocol here, print extended info
            IrReceiver.printIRResultRawFormatted(&Serial, true);
            IrReceiver.resume(); // Do it here, to preserve raw data for printing with printIRResultRawFormatted()
        } else {
            IrReceiver.resume(); // Early enable receiving of the next IR frame
            // Print decoded command to serial
            Serial.println(IrReceiver.decodedIRData.command, HEX); 
            
            // Play sound on passive buzzer 
            switch(IrReceiver.decodedIRData.command){
                case 0x40:
                    IrReceiver.stopTimer(); // Must stop the IR timer to prevent the tone function from affecting the timer
                    tone(buzzer_pin, 1500, 8);
                    delay(8);
                    IrReceiver.restartTimer(8000); 
                    break;
                case 0x46:
                case 0x15:
                case 0x44:
                case 0x43:
                    IrReceiver.stopTimer(); 
                    tone(buzzer_pin, 500, 8);
                    delay(8);
                    IrReceiver.restartTimer(8000); 
                    break;
            }
        }
    }
}