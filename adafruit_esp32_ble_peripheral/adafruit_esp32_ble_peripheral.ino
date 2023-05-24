/*
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleServer.cpp
    Ported to Arduino ESP32 by Evandro Copercini
    updates by chegewara
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <ArduinoJson.h>
#include <Adafruit_NeoPixel.h>
#include <HardwareSerial.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "f10016f6-542b-460a-ac8b-bbb0b2010596"
#define CHARACTERISTIC_UUID "f22535de-5375-44bd-8ca9-d0ea9ff9e419"
bool deviceConnected = false;
 
Adafruit_NeoPixel strip(1, 0 , NEO_GRB + NEO_KHZ800);

//HardwareSerial mySerial(1);

const int subchain_pins[12] = {5,19,21,8,7,14,32,15,33,27,12,13};
const int subchain_num = 12;
uint32_t colors[5];
int color_num = 5;

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        // get command
        std::string value = pCharacteristic->getValue();
        Serial.println(value.c_str());
        // decode JSON
        DynamicJsonDocument command(1024);
        deserializeJson(command, value);
        sendCommand(command);
    }

    /* command format
     *  command = {
            'addr':motor_addr,
            'mode':start_or_stop,
            'duty':3, # default
            'freq':2, # default
            'wave':0, # default
        }
     */
    void sendCommand(DynamicJsonDocument& command){
      int motor_addr = command["addr"].as<int>();
      int is_start = command["mode"].as<int>();
      int duty = command["duty"].as<int>();
      int freq = command["freq"].as<int>();
      int wave = command["wave"].as<int>();
      if(motor_addr>=0 && motor_addr<96){// maximum number of motor on one chain
        if(is_start == 1){//start command, two bytes
          uint8_t message[2];
          message[0] = (motor_addr << 1) + is_start;
          message[1] = 192 + (duty << 4) + (freq << 2) + wave;
          Serial1.write(message, 2);
          strip.setPixelColor(0, colors[motor_addr % color_num]);
          strip.show();
        }
        else{//stop command, only one byte
          uint8_t message = (motor_addr << 1) + is_start;
          Serial1.write(message);
          strip.setPixelColor(0, 0, 0, 0);
          strip.show();
        }
      }
      else{
        Serial.println("motor address is not in range...");
      }
    }
};

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      Serial.println("connected!");
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      Serial.println("disconnected!");
      delay(500);
      deviceConnected = false;
      BLEDevice::startAdvertising();
    }
};


void setup() {
  Serial.begin(115200);//even parity check
//  pinMode(8, OUTPUT);
//  pinMode(7, INPUT);
//  mySerial.begin(115200, SERIAL_8E1, 7, 8);
  Serial1.begin(115200, SERIAL_8E1);
  
  Serial.println("Starting BLE work!");

  Serial.println(SOC_UART_NUM);

  //setup LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  strip.begin();
  strip.setBrightness(64);
  colors[0] = strip.Color(255, 0, 0);
  colors[1] = strip.Color(0, 255, 0);
  colors[2] = strip.Color(0, 0, 255);
  colors[3] = strip.Color(255, 0, 255);
  colors[4] = strip.Color(255, 255, 0);
  strip.setPixelColor(0, colors[0]);
  strip.show();
  
  //BLE setup
  BLEDevice::init("BINGJIAN_FEATHER");
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
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");

  //actuator pin setup
//  for (int i=0; i<subchain_num; ++i){
//    pinMode(subchain_pins[i], OUTPUT);
//    digitalWrite(subchain_pins[i], LOW);
//  }
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
}
