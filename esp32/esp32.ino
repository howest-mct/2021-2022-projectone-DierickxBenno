//#include "WiFi.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include "BluetoothSerial.h"

float temperatureC;
byte LED = 2;
// inputs
const byte owTemp = 4;
OneWire oneWire(owTemp); 
DallasTemperature sensors(&oneWire);

//const char* ssid = "ssid";
//const char* pswd = "pswd";

float testList[3] = {0, 0, 0};

BluetoothSerial SerialBT;

void setup() {
  SerialBT.begin("DogBit-BD-1MCT1");
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Service started");
  
//  WiFi.begin(ssid, pswd);
}

void loop() {
  sensors.requestTemperatures();
  temperatureC = sensors.getTempCByIndex(0);
  Serial.println("test message");
  digitalWrite(LED, 1);
  delay(100);
  testList[0] = temperatureC;
  sendData(testList);
  digitalWrite(LED, 0);
}

void sendData(float pData[3]){
  SerialBT.println(String(pData[0]));
}
