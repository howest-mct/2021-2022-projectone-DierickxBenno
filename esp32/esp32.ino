// #include <WiFi.h>
#include <Wire.h>
#include <OneWire.h>
#include <BluetoothSerial.h>
#include <FastLED.h>

#define numLeds 8

CRGBArray<numLeds> leds;

byte i; // led intensity
byte pinWS2812 = 13;
int hue = 360;
String recvd_hue = "";
String strHue;

// timed events
// measure temperature/light intensity
int eventtimeTemp = 30000;
int pasteventTemp = 0;
//
byte LOplus = 41;
byte LOmin = 40;
const byte owTemp = 4;
float hoek;
bool tussenStap2 = 0;
byte stappen = 0;
int ldrPin = 34;
float lightValue;
float pastLightValue = 9999.0;
const int MPU = 0x68; // MPU6050 I2C address
int GyroY;
// bools
bool ledStatus = 0;
//
// ecg
int heartVal;
int pastHeartVal;
long startTime = millis();
long endTime = 0;
float pulse;
//

OneWire ds(owTemp);

BluetoothSerial SerialBT;

#define GPSSerial Serial2

void setup()
{
  // ecg
  pinMode(LOplus, INPUT);
  pinMode(LOmin, INPUT);
  //
  FastLED.addLeds<NEOPIXEL, 13>(leds, numLeds);
  // basic setup
  byte LED = 2;
  pinMode(LED, OUTPUT);

  Serial.begin(115200);

  // wifi setup
  // WiFi.begin(ssid, password);
  // BT setup
  SerialBT.begin("DogBit-BD-1MCT1");

  //# region MPU setup

  Wire.begin(); // Initialize comunication
  mpuWriteMsg(0x6B, 0x1);
  mpuWriteMsg(0x1c, 0x10);
  mpuWriteMsg(0x1B, 0x10);
  delay(20);

  GPSSerial.begin(9600);
}

void loop()
{
  // show loop is running
  digitalWrite(2, 1);
  delay(10);
  digitalWrite(2, 0);
  // //

  // elke 30 seconden wordt de temperatuur en licht intensiteit doorgestuurd
  if ((millis() - pasteventTemp) > eventtimeTemp)
  {
    sendTemperature();
    pasteventTemp = millis();
    getLightIntensity();
  }
  // elke 50 stappen wordt de gps data doorgestuurd
  if (stappen >= 50)
  {
    stappen = 0;
    Serial.println(stappen);
    getGPSdata();
  }

  setLedIntensity();
  detectSteps();
  setLedColor();
}

void sendTemperature()
{
  byte i;
  byte type_s;
  byte data[12];
  byte addr[8];
  float temperatureC;

  if (!ds.search(addr))
  {
    ds.reset_search();
    return;
  }

  if (OneWire::crc8(addr, 7) != addr[7])
  {
    return;
  }

  // the first ROM byte indicates which chip
  ds.reset();
  ds.select(addr);
  ds.write(0x44);

  ds.reset();
  ds.select(addr);
  ds.write(0xBE);

  for (i = 0; i < 9; i++)
  {
    data[i] = ds.read();
  }

  int16_t raw = (data[1] << 8) | data[0];
  if (type_s)
  {
    raw = raw << 3;
    if (data[7] == 0x10)
    {
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  }
  else
  {
    byte cfg = (data[4] & 0x60);
    if (cfg == 0x00)
      raw = raw & ~7;
    else if (cfg == 0x20)
      raw = raw & ~3;
    else if (cfg == 0x40)
      raw = raw & ~1;
  }
  temperatureC = (float)raw / 16.0;
  SerialBT.println("temperatuur: " + String(temperatureC));
}

// #region step counter
void mpuWriteMsg(int regAdres, int msg)
{
  Wire.beginTransmission(MPU);
  Wire.write(regAdres);
  Wire.write(msg);
  Wire.endTransmission(true);
}

void mpuDataRequest(int regAdres, int bytes)
{
  Wire.beginTransmission(MPU);
  Wire.write(regAdres);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, bytes, true);
}

void detectSteps()
{
  mpuDataRequest(0x45, 6);
  GyroY = (Wire.read() << 8 | Wire.read());
  if (((GyroY & 0x8000) >> 15) == 1)
  {
    hoek = (GyroY - 0xffff) / 131.0;
  }
  else
  {
    hoek = GyroY / 131.0;
  }

  float corner = 12.22;
  /* Get new sensor events with the readings */

  // code for step counter
  if (hoek < (-1 * corner))
  {
    tussenStap2 = 1;
  }

  if ((hoek > corner) && (tussenStap2 == 1))
  {
    tussenStap2 = 0;
    stappen += 1;
    SerialBT.println("\nstappen +1");
  }
}
//

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
  // Serial.println(analogRead(ldrPin));

  if (lightValue <= 75)
  {
    if (abs(lightValue - pastLightValue) > 10)
    {
      pastLightValue = lightValue * 1.0; // *1.0 zodat het zeker float blijft
      i = ((100 - lightValue) / 100) * 255;
      for (byte j = 0; j < numLeds; j++)
      {
        leds[i] = CHSV(hue, 255, 255);
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

void measureECG()
{
  if ((digitalRead(LOplus) == 1) || (digitalRead(LOmin) == 1))
  {
    Serial.println('!');
  }
  else
  {
    heartVal = analogRead(A0);
    //        Serial.println(heartVal);
    if (heartVal > 2500)
    {
      heartVal = analogRead(A0);
      if (heartVal < pastHeartVal)
      {
        if (endTime != startTime)
        {
          pulse = 300 / ((startTime - endTime) / (200.0));
          //          Serial.println(pulse);
          SerialBT.println("pulse: " + String(pulse));
        }
      }
      pastHeartVal = heartVal;
      endTime = startTime;
    }
    else
    {
      startTime = millis();
    }
  }
}

void setLedColor()
{

  while (SerialBT.available())
  {
    // Serial.println("ontvangen");
    // Serial.write(SerialBT.read());
    char c = SerialBT.read();
    recvd_hue += c;
    // Serial.write(c);
  }
  if (recvd_hue != "")
  {
    for (byte i = 5; i <= 9; i++)
    {
      strHue += recvd_hue[i];
      Serial.println(strHue);
      // Serial.println(recvd_hue[i]);
    }
    Serial.print('.');
    hue = strHue.toInt();
    Serial.println('hue is: ' + String(hue));
  }
  recvd_hue = "";
}