#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLEClient.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "f10016f6-542b-460a-ac8b-bbb0b2010599"
#define CHARACTERISTIC_UUID "f22535de-5375-44bd-8ca9-d0ea9ff9e410"
#define CURRENTSENSING_UUID "640b8bf5-3c88-44f6-95e0-f5813b390d73"
BLECharacteristic *csCharacteristic;

bool deviceConnected = false;

Adafruit_NeoPixel strip(1, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);

const int subchain_pins[4] = {18, 17, 9, 8};
const int subchain_num = 4;
uint32_t colors[5];
int color_num = 5;
int global_counter = 0;

EspSoftwareSerial::UART serial_group[4];

bool isTriggered = false;
unsigned long triggerTime = 0;
sensors_event_t triggerEvent;
sensors_event_t lastEvent; 

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
      String value = pCharacteristic->getValue();
      if (value.length() % 3 == 0) {  // Ensure the length is a multiple of 3 bytes
          unsigned long timestamp = millis(); // Get current time in milliseconds
          Serial.print("Timestamp: ");
          Serial.print(timestamp);
          Serial.print(" ms, Data = ");
          Serial.print(value.length());
          Serial.print(" bytes, # = ");
          Serial.println(++global_counter);
  
          for (int i = 0; i < value.length(); i += 3) {
              uint8_t byte1 = value[i];
              uint8_t byte2 = value[i+1];
              uint8_t byte3 = value[i+2];
  
              if (byte1 == 0xFF) continue; // Skip if the first byte of the command is 0xFF
  
              int serial_group_number = (byte1 >> 2) & 0x0F;
              int is_start = byte1 & 0x01;
              int addr = byte2 & 0x3F;
              int duty = (byte3 >> 3) & 0x0F;
              int freq = (byte3 >> 1) & 0x03;
              int wave = byte3 & 0x01;
  
              // Print received values for debugging
              // Uncomment the following lines if you want to output the values for debugging purposes
              
//              Serial.print("Received: ");
//              Serial.print("SG: "); Serial.print(serial_group_number);
//              Serial.print(", Mode: "); Serial.print(is_start);
//              Serial.print(", Addr: "); Serial.print(addr);
//              Serial.print(", Duty: "); Serial.print(duty);
//              Serial.print(", Freq: "); Serial.print(freq);
//              Serial.print(", Wave: "); Serial.println(wave);
              
              
              sendCommand(serial_group_number, addr, is_start, duty, freq, wave);
          }
      }
      else{
          unsigned long timestamp = millis(); // Get current time in milliseconds
          Serial.print("Timestamp: ");
          Serial.print(timestamp);
          Serial.print(" ms, Data = ");
          Serial.print(value.length());
          Serial.print(", WRONG LENGTH!!!!!!!!!!!!!!!!");
      }
  }


    /* command format
        command = {
            'addr':motor_addr,
            'mode':start_or_stop,
            'duty':3, # default
            'freq':2, # default
            'wave':0, # default
        }
    */
    void sendCommand(int serial_group_number, int motor_addr, int is_start, int duty, int freq, int wave) {
//      uint8_t message = motor_addr;
//      serial_group[serial_group_number].write(message);
//      return;
      if (is_start == 1) { // Start command, two bytes
        isTriggered = true;
        triggerTime = millis();
        triggerEvent.acceleration = lastEvent.acceleration;
        Serial.print("trigger time (ms) = ");
        Serial.println(triggerTime);
        uint8_t message[2];
        message[0] = (motor_addr << 1) | is_start;
        message[1] = 0x80 | (duty << 3) | (freq << 1) | wave;
        serial_group[serial_group_number].write(message, 2);
      } else { // Stop command, only one byte
        isTriggered = false;
        uint8_t message = (motor_addr << 1) | is_start;
        serial_group[serial_group_number].write(&message, 1);
      }
    }
};


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer, esp_ble_gatts_cb_param_t *param){
        Serial.println("connected!");
        Serial.println(BLEDevice::toString().c_str());
        char bda_str[18];
        sprintf(bda_str, "%02X:%02X:%02X:%02X:%02X:%02X", param->connect.remote_bda[0], param->connect.remote_bda[1], param->connect.remote_bda[2], param->connect.remote_bda[3], param->connect.remote_bda[4], param->connect.remote_bda[5]);
        Serial.println("Device connected with Address: " + String(bda_str));
        pServer->updateConnParams(param->connect.remote_bda, 0, 0, 0, 100);
        deviceConnected = true;
    }

    void onDisconnect(BLEServer* pServer) {
      Serial.println("disconnected!");
      delay(500);
      deviceConnected = false;
      BLEDevice::startAdvertising();
    }
};

unsigned long lastTimestamp;
unsigned long counter;

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(0xE5);
char outputChar[40];

void setup(void) 
{
  /*
   * initialize acceleromter ADXL345
   */
    
  #ifndef ESP8266
    while (!Serial); // for Leonardo/Micro/Zero
  #endif
  //  Serial.begin(115200);
  //  Serial.println("Accelerometer Test"); Serial.println("");
    
  /* Initialise the sensor */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }

  /* Set the range to whatever is appropriate for your project */
  
  accel.setRange(ADXL345_RANGE_16_G);
  accel.setDataRate(ADXL345_DATARATE_3200_HZ);
  counter = 0;
  lastTimestamp = millis();

  
  /* 
   *  initialize BLE peripheral
   */
  Serial.begin(500000);//even parity check
  //  pinMode(8, OUTPUT);
  //  pinMode(7, INPUT);
  //  Serial1.begin(115200, SERIAL_8E1);// Hardware Serial
  Serial.print("number of hardware serial available: ");
  Serial.println(SOC_UART_NUM);
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
  Serial.println("Starting BLE work!");

  //setup LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
    strip.begin();
    strip.setBrightness(20);
    colors[0] = strip.Color(0, 255, 0);
    strip.setPixelColor(0, colors[0]);
    strip.show();

  //BLE setup
  BLEDevice::init("QT Py ESP32-S3");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pCharacteristic->setValue("0");
  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());
  pService->start();

  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");

}

float accDiff(sensors_vec_t acc1, sensors_vec_t acc2) {
  float diffX = acc1.x - acc2.x;
  float diffY = acc1.y - acc2.y;
  float diffZ = acc1.z - acc2.z;
  return sqrt(diffX * diffX + diffY * diffY + diffZ * diffZ);
}

void loop(void) 
{
  /* Get a new sensor event */
  sensors_event_t event; 
  accel.getEventXYZ(&event);
  lastEvent.acceleration = event.acceleration;

  if(isTriggered){
    if(accDiff(event.acceleration, triggerEvent.acceleration) > 2.0){
      unsigned long currentTime = millis();
      Serial.print("response time (ms) = ");
      Serial.println(currentTime);
      Serial.print("diff = ");
      Serial.println(currentTime - triggerTime);
      String outputString = "{\"X\":"+String(triggerEvent.acceleration.x, 2)+",\"Y\":"+String(triggerEvent.acceleration.y, 2)+",\"Z\":"+String(triggerEvent.acceleration.z, 2)+"}\n";
      memset(outputChar, 0, sizeof(char)*40);
      outputString.toCharArray(outputChar, outputString.length()+1);
      Serial.write(outputChar, 40);
      outputString = "{\"X\":"+String(event.acceleration.x, 2)+",\"Y\":"+String(event.acceleration.y, 2)+",\"Z\":"+String(event.acceleration.z, 2)+"}\n";
      memset(outputChar, 0, sizeof(char)*40);
      outputString.toCharArray(outputChar, outputString.length()+1);
      Serial.write(outputChar, 40);
      isTriggered = false;
    }
  }
}
