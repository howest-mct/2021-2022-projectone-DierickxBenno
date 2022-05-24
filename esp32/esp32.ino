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
float hoek;
bool tussenStap = 0;
bool tussenStap2 = 0;
int stappen = 0;

OneWire oneWire(owTemp);
DallasTemperature sensors(&oneWire);

Adafruit_MPU6050 mpu;

// const char* ssid = "ssid";
// const char* pswd = "pswd";

float testList[3] = {0, 0, 0};

BluetoothSerial SerialBT;

// #region timed events
int eventtimeTemp = 1000;
long pasteventTemp = 0;

void setup()
{
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
  if (!mpu.begin())
  {
    Serial.println("Failed to find MPU6050 chip");
    while (1)
    {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  // # endregion MPU setup

  sensors.begin();
  Serial.println("Service started");

  //  WiFi.begin(ssid, pswd);
}

void loop()
{
  digitalWrite(LED, 1);
  if ((millis() - pasteventTemp) > eventtimeTemp)
  {
    sendTemperature();
    pasteventTemp = millis();
  }
  digitalWrite(LED, 0);
  detectSteps();
  delay(10);
}

void sendTemperature()
{
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
  if (hoek < 0.15)
  {
    tussenStap2 = 1;
  }

  if (hoek > 0.15 && tussenStap2 == 1)
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