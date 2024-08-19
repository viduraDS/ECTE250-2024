/* Author: Brian Lambert */

#ifndef BN880Decoder_h
#define BN880Decoder_h

/*-----( Import needed libraries )-----*/
#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/*-----( Declare Constants and Pin Numbers )-----*/

#define GPSBAUD 9600
#define START_SENTENCE '$'
#define DATA_BUFFER_SIZE 250



class BN880Decoder
{
/*-----( Declare Variables and functions )-----*/
  public:
	BN880Decoder();
	void begin();
	void readRawData();
	void printDataBuffer();
	String getSentence(String type);
	bool getContentsGNGGA();
	String sentence = "";
	String hours = "";
	String minutes = "";
	String seconds = "";
	float latitude = 0.0;
	float longitude = 0.0;
	String hemisphereNS = "";
	String hemisphereEW = "";
	String gpsFix = "";
	float satellites = 0.0;
	float hdop = 0.0;
	float altitude = 0.0;
	float geoidHeight = 0.0;
	
	
	

  private:
	
	char dataBuffer[DATA_BUFFER_SIZE];
	float stringToFloat(String input);
	bool NMEAchecksum( String input, int cnt );
	int getSentenceIndex(String type, int from);
	
	
};

#endif
