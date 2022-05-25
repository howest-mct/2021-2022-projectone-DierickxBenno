// #include "WiFi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <BluetoothSerial.h>

// timed events
int eventtimeTemp = 5000;
int pasteventTemp = 0;
//
const byte owTemp = 4;
float hoek;
bool tussenStap = 0;
bool tussenStap2 = 0;
int stappen = 0;

OneWire oneWire(owTemp);
DallasTemperature sensors(&oneWire);

Adafruit_MPU6050 mpu;

// voor OTA

BluetoothSerial SerialBT;

void setup()
{
  /*
   * Login page
   */

  // basic setup
  byte LED = 2;
  pinMode(LED, OUTPUT);
  Serial.begin(115200);

  // wifi setup
  // WiFi.begin(ssid, password);
  // BT setup
  SerialBT.begin("DogBit-BD-1MCT1");

  //# region MPU setup
  while (!Serial)
  {
    delay(10);
  } // will pause Zero, Leonardo, etc until serial console opens

  // mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  // # endregion MPU setup

  sensors.begin();
}

void loop()
{
  // show loop is running
  digitalWrite(2, 1);
  delay(10);
  digitalWrite(2, 0);
  //
  if ((millis() - pasteventTemp) > eventtimeTemp)
  {

    sendTemperature();
    pasteventTemp = millis();
  }

  detectSteps();
}

void sendTemperature()
{
  float temperatureC;
  sensors.requestTemperatures();
  temperatureC = sensors.getTempCByIndex(0);
  SerialBT.println("temperatuur: " + String(temperatureC));
}

void detectSteps()
{
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  hoek = g.gyro.y;
  // code for step counter
  if (hoek < 0.4)
  {
    tussenStap2 = 1;
  }

  if (hoek > 0.4 && tussenStap2 == 1)
  {
    tussenStap2 = 2;
    tussenStap = !tussenStap;
    if (tussenStap)
    {
      SerialBT.println("stappen +1");
      Serial.println("stap genomen");
    }
  }
}
