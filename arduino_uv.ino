#include <SPI.h>


//sensor input pin
#define INPIN A0

//raw input from sensor 
int raw;
//calculated voltage value from sensor raw value
int voltage;
//uv index, calculated from datasheet
int uvi;
//debug output for serial monitor
int debug;



void setup(){
  Serial.begin(9600);

  //initiate SPI in slave mode
  SPCR |= bit(SPE);
  
  //set master/slave, output/input
  pinMode(MISO, OUTPUT);
  pinMode(MOSI, INPUT);
  
  //initiate SPI transaction
  SPI.beginTransaction(SPISettings(1024, MSBFIRST, SPI_MODE0));
}

void loop(){
  read_uv();

  //send uv index as byte array to RPi once a second
  pinMode(SS, LOW);
  debug = SPI.transfer(get_uvi());
  Serial.println(debug);
  pinMode(SS, HIGH);
  
  delay(1000);
}



//read from uv sensor on INPIN and calculate/return voltage
int read_uv(){
  raw = analogRead(INPIN);
  voltage = (raw * (5.0 / 1023.0)) * 1000;
  return voltage;
}

//determine uv index from datasheet with conditionals
int get_uvi(){
  if(voltage < 226){uvi = 0;}
  else if (voltage < 318) {uvi = 1;}
  else if (voltage < 408) {uvi = 2;}
  else if (voltage < 503) {uvi = 3;}
  else if (voltage < 606) {uvi = 4;}
  else if (voltage < 696) {uvi = 5;}
  else if (voltage < 795) {uvi = 6;}
  else if (voltage < 881) {uvi = 7;}
  else if (voltage < 976) {uvi = 8;}
  else if (voltage < 1079)  {uvi = 9;}
  else if (voltage < 1170)  {uvi = 10;}
  else if (voltage > 1170)  {uvi = 11;}
  else {uvi = 0;}
  
  return uvi;
}
