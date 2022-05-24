// #include "WiFi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <BluetoothSerial.h>

float temperatureC;
byte LED = 2;
const byte owTemp = 4;

OneWire oneWire(owTemp); 
DallasTemperature sensors(&oneWire);

Adafruit_MPU6050 mpu;

//const char* ssid = "ssid";
//const char* pswd = "pswd";

float testList[3] = {0, 0, 0};

BluetoothSerial SerialBT;

void setup() {
  SerialBT.begin("DogBit-BD-1MCT1");
  pinMode(LED, OUTPUT);
  Serial.begin(115200);

  // #region MPU setup
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  // # endregion MPU setup

  sensors.begin();
  Serial.println("Service started");
  
  
//  WiFi.begin(ssid, pswd);
}

void loop() {
  sensors.requestTemperatures();
  temperatureC = sensors.getTempCByIndex(0);
  Serial.println("test message");
  digitalWrite(LED, 1);
  delay(150);
  testList[0] = temperatureC;
  sendData(testList);
  digitalWrite(LED, 0);
  getMPU();
}

void sendData(float pData[3]){
  SerialBT.println(String(pData[0]));
}


void getMPU () {
/* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");
}