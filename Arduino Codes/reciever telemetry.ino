#include <SoftwareSerial.h>

SoftwareSerial telemetrySerial(10,11 ); // Create a software serial object for telemetry reception

struct TelemetryData { // Define a struct to hold the telemetry data
  double mctempmotor;
  double mctempcontroller;
  double pack_current;
  double pack_inst_voltage;
  double state_of_charge;
  double high_temp;
  double low_temp;
};

void setup() {
  Serial.begin(9600); // Initialize the serial port for debugging
  telemetrySerial.begin(9600); // Initialize the telemetry serial port
}

void loop() {
  if (telemetrySerial.available() >= sizeof(TelemetryData)) { // Check if a full telemetry packet has been received
    byte dataBytes[sizeof(TelemetryData)];
    telemetrySerial.readBytes(dataBytes, sizeof(dataBytes)); // Read the telemetry packet into a byte array

    TelemetryData data; // Create a TelemetryData object to hold the received data
    memcpy(&data, dataBytes, sizeof(data)); // Decapsulate the received data into the TelemetryData object
    
    Serial.println("Received telemetry data: ");
    Serial.print("mctempmotor: ");
    Serial.println(data.mctempmotor);
    Serial.print("mctempcontroller: ");
    Serial.println(data.mctempcontroller);
    Serial.print("Pack current: ");
    Serial.println(data.pack_current);
    Serial.print(" Pack instantaneous voltage: ");
    Serial.println(data.pack_inst_voltage);
    Serial.print(" State of charge: ");
    Serial.println(data.state_of_charge);
    Serial.print(" High temperature: ");
    Serial.println(data.high_temp);
    Serial.print(" Low temperature: ");
    Serial.println(data.low_temp);
    // Use the received telemetry data to do something
  }
}