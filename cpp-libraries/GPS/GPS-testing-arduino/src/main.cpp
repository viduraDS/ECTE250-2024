#include <Arduino.h>
#include <BN880Decoder.h>

// put function declarations here:
int myFunction(int, int);

BN880Decoder decoder;

void setup() {
  // put your setup code here, to run once:
  decoder.begin();
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  decoder.readRawData();
  String result = (decoder.getSentence("GNGGA"));
  if(result != "")
      {
        Serial.println(result);
      } 
  if(decoder.getContentsGNGGA());
    {
      Serial.print(F("Time "));
        Serial.print(decoder.hours);
        Serial.print(F(":"));
        Serial.print(decoder.minutes);
        Serial.print(F(":"));
        Serial.print(decoder.seconds);
        Serial.println();
        Serial.print(F("Latitude "));

      if(decoder.hemisphereNS == "N")
          {
            Serial.print(decoder.latitude,6);
          }
        else
          {
            Serial.print(-decoder.latitude,6);
          }
        Serial.println(" " + decoder.hemisphereNS);
        Serial.print(F("Longitude "));
        if(decoder.hemisphereEW == "E")
          {
            Serial.print(decoder.longitude,7);
          }
        else
          {
            Serial.print(-decoder.longitude,7);
          }
        Serial.println(" " + decoder.hemisphereEW);
        Serial.print(F("GPS fix "));
        if(decoder.gpsFix == "0")
          {
            Serial.println(F("Bad"));
          }
        else
          {
            Serial.println(F("Good"));
          }
        Serial.print(F("Satellites "));
        Serial.println(decoder.satellites,0);
        Serial.print(F("Horizontal dilution of precision "));
        Serial.println(decoder.hdop,2);
        Serial.print(F("Altitude "));
        Serial.print(decoder.altitude, 1);
        Serial.println(F(" metres"));
        Serial.print(F("Height of geoid above WGS84 ellipsoid "));
        Serial.print(-decoder.geoidHeight, 1);
        Serial.println(F(" metres"));
        Serial.println(F("***********************"));

    }
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}