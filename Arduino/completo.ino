#include <OneWire.h>
#include <DallasTemperature.h>    
#include <ZMPT101B.h>

#define SENSITIVITY 500.0f

#define ONE_WIRE_BUS_TEMP 2   // Pin para el sensor de temperatura DS18B20 2 Digital

// ZMPT101B sensor output connected to analog pin A0
// and the voltage source frequency is 50 Hz.
ZMPT101B voltageSensor(A1, 50.0);

OneWire oneWire(ONE_WIRE_BUS_TEMP);
DallasTemperature sensors(&oneWire);

// Sensor de Corriente colocar en A0, el pin 0 Analogico
const int sensorPin = 14;     // initializing a pin for the sensor output


void setup() {
  Serial.begin(9600);

  voltageSensor.setSensitivity(SENSITIVITY);

  pinMode(sensorPin, INPUT);

  sensors.begin();
}

void loop() {

  // read the voltage and then print via Serial.
  analogReference(DEFAULT);
  float voltage = voltageSensor.getRmsVoltage();
  Serial.print(voltage);

  // Sensor de Temperatura DS18B20
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0); // Obtener temperatura en grados Celsius
  Serial.print(" ");
  Serial.print(temperatureC);

  // Sensor de Corriente
  analogReference(INTERNAL);
  Serial.print(" ");
  float Irms=get_corriente(); //Corriente eficaz (A)
  Irms = Irms;
  Serial.println(Irms,3);

  Serial.println();

  delay(100); // Esperar un segundo antes de la siguiente lectura
}


float get_corriente()
{
  float voltajeSensor;
  float corriente=0;
  float Sumatoria=0;
  long tiempo=millis();
  int N=0;
  while(millis()-tiempo<50)//Duración 0.5 segundos(Aprox. 30 ciclos de 60Hz)
  { 
    voltajeSensor = analogRead(A0) * (1.1 / 1023.0);////voltaje del sensor
    corriente=voltajeSensor*30.0; //corriente=VoltajeSensor*(30A/1V)
    Sumatoria=Sumatoria+sq(corriente);//Sumatoria de Cuadrados
    N=N+1;
    delay(1);
  }
  Sumatoria=Sumatoria*2;//Para compensar los cuadrados de los semiciclos negativos.
  corriente=sqrt((Sumatoria)/N); //ecuación del RMS
  return(corriente);
}