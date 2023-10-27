#include "EmonLib.h" 
EnergyMonitor emon1;

void setup() {
  // put your setup code here, to run once:
  emon1.voltage(A0,187,1.7);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  emon1.calcVI(20,2000);
  int Voltage = emon1.Vrms;
  Serial.print(Voltage);
  Serial.print(" ");

  float temperature = Voltage * 0.3;
  Serial.print(temperature);
  Serial.print(" ");

  float rpm = Voltage * 10;
  Serial.print(rpm);
  Serial.print(" ");

  float corriente = Voltage / 100;
  Serial.print(corriente);
  Serial.println();

  delay(500);
}
