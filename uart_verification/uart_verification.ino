unsigned long totalReceived = 0;
unsigned long errorCount = 0;
int currentIndex = 0;

void setup() {
  // Initialize Serial1 with specified configurations
  Serial1.begin(500000, SERIAL_8E1, 18, 17, false);
  Serial.begin(500000);  // Initialize debugging serial port

  // Print initialization message
  Serial.println("UART communication initialized.");
}

void loop() {
  if (Serial1.available()) {  // Check if data is available to read
    int received = (int)(Serial1.read());  // Read a byte

    totalReceived++;  // Increment total received messages count
//    Serial.print("received = "); Serial.println(received);
//    Serial.print("current = "); Serial.println(currentIndex);
    if(currentIndex != received){
      errorCount++;
    }
    currentIndex = (currentIndex + 1) % 30;

    // Calculate and display error rate
    float errorRate = 100.0 * errorCount / totalReceived;
    if(totalReceived % 100 == 0){
      Serial.print("total count = "); Serial.print(totalReceived);
      Serial.print(", error rate = "); Serial.print(errorRate); Serial.println("%");
    }
  }
}
