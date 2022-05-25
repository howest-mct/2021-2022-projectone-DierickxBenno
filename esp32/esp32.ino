// #include "WiFi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
// #include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <BluetoothSerial.h>

// timed events
int eventtimeTemp = 100;
int pasteventTemp = 0;
//
const byte owTemp = 4;
float hoek;
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

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin())
  {
    Serial.println("Failed to find MPU6050 chip");
    while (1)
    {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
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
  float corner = .12;
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  hoek = g.gyro.y;
  // Serial.println(hoek);
  // code for step counter
  if (hoek < (-1 * corner))
  {
    tussenStap2 = 1;
    // Serial.println("tussenstap2");
  }

  if ((hoek > corner) && (tussenStap2 == 1))
  {
    // Serial.println("tussenstap1");
    tussenStap2 = 0;
    stappen += 1;
    Serial.println(stappen);
    SerialBT.println("stappen +1");
    Serial.println("stap genomen");
  }
}
