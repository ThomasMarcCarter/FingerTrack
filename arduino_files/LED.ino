void setup() {
    pinMode(13, OUTPUT); // set the LED pin as an output
    Serial.begin(9600);  // initialize serial communication at 9600 bits per second
}

void loop() {
    if (Serial.available() > 0) { // check if there is data available on the serial port
        int incomingByte = Serial.read(); // read the incoming byte
        if (incomingByte == '1') {
            digitalWrite(13, HIGH); // turn the LED on
        }
        else if (incomingByte == '0') {
            digitalWrite(13, LOW); // turn the LED off
        }
    }
}