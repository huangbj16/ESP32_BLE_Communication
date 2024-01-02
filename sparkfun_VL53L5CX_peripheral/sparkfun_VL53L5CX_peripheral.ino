#include <SoftwareSerial.h>
#include <Wire.h>
#include <SparkFun_VL53L5CX_Library.h> //http://librarymanager/All#SparkFun_VL53L5CX

// ToF sensor objects
SparkFun_VL53L5CX myImager;
VL53L5CX_ResultsData measurementData; // Result data class structure, 1356 byes of RAM
int imageResolution = 0; // Used to pretty print output
int imageWidth = 0;      // Used to pretty print output
long measurements = 0;         // Used to calculate actual output rate
long measurementStartTime = 0; // Used to calculate actual output rate


// serial chain setup
const int subchain_pins[8] = {26, 25, 5, 19, 21, 14, 32, 15};
const int actuator_unit[16] = {7,4,37,34,8,3,38,33,9,2,39,32,10,1,40,31};
bool is_triggered[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
const int subchain_num = 8;

EspSoftwareSerial::UART serial_group[8];


void sendCommand(int motor_addr, int is_start = 0, int duty = 7, int freq = 2, int wave = 0) {
  int send_motor_addr = motor_addr % 30;
  int serial_group_number = motor_addr / 30;
  if (motor_addr >= 0 && motor_addr < 256) { // maximum number of motor on one chain
    if (is_start == 1) { //start command, two bytes
      uint8_t message[2];
      message[0] = ((send_motor_addr) << 1) + is_start;
      message[1] = 128 + (duty << 3) + (freq << 1) + wave;
      serial_group[serial_group_number].write(message, 2);
    }
    else { //stop command, only one byte
      uint8_t message = (send_motor_addr << 1) + is_start;
      serial_group[serial_group_number].write(message);
    }
  }
  else {
    Serial.println("motor address is not in range...");
  }
}



void setup()
{
  Serial.begin(115200);
  delay(1000);
  Serial.println("SparkFun VL53L5CX Imager Example");

  Wire.begin(); // This resets I2C bus to 100kHz
  Wire.setClock(400000); //Sensor has max I2C freq of 1MHz

  // myImager.setWireMaxPacketSize(128); // Increase default from 32 bytes to 128 - not supported on all platforms

  Serial.println("Initializing sensor board. This can take up to 10s. Please wait.");
  if (myImager.begin() == false)
  {
    Serial.println(F("Sensor not found - check your wiring. Freezing"));
    while (1)
      ;
  }

  myImager.setResolution(4 * 4); // Enable all 64 pads

  imageResolution = myImager.getResolution(); // Query sensor for current resolution - either 4x4 or 8x8
  imageWidth = sqrt(imageResolution);         // Calculate printing width

  // Using 4x4, min frequency is 1Hz and max is 60Hz
  // Using 8x8, min frequency is 1Hz and max is 15Hz
  myImager.setRangingFrequency(60);

  myImager.startRanging();

  measurementStartTime = millis();


  Serial.println("Setup Software Serial");
  for (int i = 0; i < subchain_num; ++i) {
    Serial.print("initialize uart on ");
    Serial.println(subchain_pins[i]);
    serial_group[i].begin(115200, SWSERIAL_8E1, -1, subchain_pins[i], false);
    serial_group[i].enableIntTx(false);
    if (!serial_group[i]) { // If the object did not initialize, then its configuration is invalid
      Serial.println("Invalid EspSoftwareSerial pin configuration, check config");
    }
    delay(200);
  }
  Serial.println("Software Serial Setup Finished!");

  // turn on buck converter and test vibrations
  sendCommand(0, 1, 7);
  sendCommand(1, 1, 7);
  delay(1000);
  sendCommand(1, 0);
  sendCommand(30, 1, 7);
  sendCommand(31, 1, 7);
  delay(1000);
  sendCommand(31, 0);
}


void loop()
{
  // Poll sensor for new data
  if (myImager.isDataReady() == true)
  {
    if (myImager.getRangingData(&measurementData)) // Read distance data into array
    {
      // The ST library returns the data transposed from zone mapping shown in datasheet
      // Pretty-print data with increasing y, decreasing x to reflect reality
      for(int i=0; i< imageResolution; ++i){
        if(measurementData.target_status[i] != 255 && measurementData.nb_target_detected[i] != 0){
          int distance = measurementData.distance_mm[i];
          Serial.print(i);
          Serial.print(", ");
          Serial.println(distance);
          int motor_addr = actuator_unit[i];
          if(distance <= 1000){
            if(!is_triggered[i]){
              is_triggered[i] = true;
              sendCommand(motor_addr, 1, 7);
              Serial.println("start");
            }
          }
          else{
            if(is_triggered[i]){
              is_triggered[i] = false;
              sendCommand(motor_addr, 0);
              Serial.println("stop");
            }
          }
        }
        else{//zone out of range
          int motor_addr = actuator_unit[i];
          Serial.print(i);
          Serial.println(", XXX");
          if(is_triggered[i]){
              is_triggered[i] = false;
              sendCommand(motor_addr, 0);
              Serial.println("stop");
            }
        }
      }

      // Uncomment to display actual measurement rate
//       measurements++;
//       float measurementTime = (millis() - measurementStartTime) / 1000.0;
//       Serial.print("rate: ");
//       Serial.print(measurements / measurementTime, 3);
//       Serial.println("Hz");
    }
  }

  delay(5); // Small delay between polling
}
