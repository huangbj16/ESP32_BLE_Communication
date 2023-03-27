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
#include <SoftwareSerial.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "f10016f6-542b-460a-ac8b-bbb0b2010596"
#define CHARACTERISTIC_UUID "f22535de-5375-44bd-8ca9-d0ea9ff9e419"
bool deviceConnected = false;

Adafruit_NeoPixel strip(1, 0 , NEO_GRB + NEO_KHZ800);

const int actuator_pins[10] = {13,12,27,33,15,32,14,20,26,25};
int actuator_num = 10;
uint32_t colors[5];
int color_num = 5;
int count_timer = 0;

class MyCharacteristicCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        // get command
        std::string value = pCharacteristic->getValue();
        Serial.println(value.c_str());
        // decode JSON
        DynamicJsonDocument command(1024);
        deserializeJson(command, value);
        
        int motor_addr = command["addr"].as<int>();
        Serial.println(motor_addr);
        if(motor_addr>=0 && motor_addr<5){
            for(int i=0; i<actuator_num; ++i){
              digitalWrite(actuator_pins[i], LOW);
            }
            digitalWrite(actuator_pins[2*motor_addr], HIGH);
            strip.setPixelColor(0, colors[motor_addr]);
            strip.show();
            count_timer = 10;
        }
        else{
          Serial.println("input is not in range...");
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
  Serial.begin(115200, SERIAL_8E1);//even parity check
  Serial.println("Starting BLE work!");

  //setup LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  strip.begin();
  strip.setBrightness(64);
  strip.show();
  colors[0] = strip.Color(255, 0, 0);
  colors[1] = strip.Color(0, 255, 0);
  colors[2] = strip.Color(0, 0, 255);
  colors[3] = strip.Color(255, 0, 255);
  colors[4] = strip.Color(255, 255, 0);
  
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
  for (int i=0; i<actuator_num; ++i){
    pinMode(actuator_pins[i], OUTPUT);
    digitalWrite(actuator_pins[i], LOW);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(count_timer>0){
    count_timer--;
    if(count_timer == 0){
      for(int i=0; i<actuator_num; ++i){
        digitalWrite(actuator_pins[i], LOW);
      }
      strip.setPixelColor(0, 0, 0, 0);
      strip.show();
    }
  }
  delay(100);
}
