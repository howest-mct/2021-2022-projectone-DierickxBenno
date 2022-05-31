// #include <WiFi.h>
// #include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <BluetoothSerial.h>
#include <FastLED.h>

#define numLeds 8

CRGBArray<numLeds> leds;

byte i; // led intensity
byte pinWS2812 = 13;

// timed events
// measure temperature/light intensity
int eventtimeTemp = 5000 * 60;
int pasteventTemp = 0;
//
const byte owTemp = 4;
float hoek;
bool tussenStap2 = 0;
byte stappen = 0;
int ldrPin = 34;
float lightValue;
float pastLightValue = 9999.0;
// bools
bool ledStatus = 0;
//

OneWire oneWire(owTemp);
DallasTemperature sensors(&oneWire);

Adafruit_MPU6050 mpu;

BluetoothSerial SerialBT;

#define GPSSerial Serial2

void setup()
{
  FastLED.addLeds<NEOPIXEL, 13>(leds, numLeds);
  // basic setup
  byte LED = 2;
  pinMode(LED, OUTPUT);
  while (!Serial)
    ;
  Serial.begin(115200);

  // wifi setup
  // WiFi.begin(ssid, password);
  // BT setup
  SerialBT.begin("DogBit-BD-1MCT1");

  //# region MPU setup

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

  GPSSerial.begin(9600);

  sensors.begin();
}

void loop()
{
  // show loop is running
  digitalWrite(2, 1);
  delay(10);
  digitalWrite(2, 0);
  // //
  if ((millis() - pasteventTemp) > eventtimeTemp)
  {
    sendTemperature();
    pasteventTemp = millis();
    getLightIntensity();
  }

  if (stappen >= 50)
  {
    stappen = 0;
    Serial.println(stappen);
    getGPSdata();
  }

  setLedIntensity();
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

  // code for step counter
  if (hoek < (-1 * corner))
  {
    tussenStap2 = 1;
  }

  if ((hoek > corner) && (tussenStap2 == 1))
  {
    tussenStap2 = 0;
    stappen += 1;
    // SerialBT.println("\n");
    SerialBT.println("\nstappen +1");
  }
}

void getGPSdata()
{

  while ((Serial.available()) or (GPSSerial.available()))
  {
    while (Serial.available())
    {
      char c = Serial.read();
      GPSSerial.write(c);
    }
    while (GPSSerial.available())
    {
      char c = GPSSerial.read();
      Serial.write(c);
      SerialBT.print(c);
    }
  }
}

void getLightIntensity()
{
  lightValue = analogRead(ldrPin);
  SerialBT.println("LI: " + String((lightValue / 4095) * 100));
}

void setLedIntensity()
{
  lightValue = ((analogRead(ldrPin) / 4095.0) * 100.0);
  Serial.println(analogRead(ldrPin));

  if (lightValue <= 75)
  {
    if (abs(lightValue - pastLightValue) > 10)
    {
      pastLightValue = lightValue*1.0; // *1.0 zodat het zeker float blijft
      i = ((100-lightValue)/100)*255;
      for (byte j = 0; j < numLeds; j++)
      {
        leds[j] = CRGB(i, i, i);
      }
        FastLED.show();
        ledStatus = 1;
    }
  }
  else
  {
    pastLightValue = 85.0;
    for (byte j = 0; j < numLeds; j++)
    {
      leds[j] = CRGB(0, 0, 0);
    }
      FastLED.show();
      ledStatus = 0;
  }
}
