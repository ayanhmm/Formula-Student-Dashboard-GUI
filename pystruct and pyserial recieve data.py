import serial
import struct

# Configure the serial connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate port and 9600 with the baud rate of your Arduino

# Read data from Arduino
while True:
    try:
        # Read 4 bytes of data from the serial port
        data_bytes = ser.read(4)
        
        # Interpret the received bytes as a float
        data_float = struct.unpack('f', data_bytes)[0]
        
        # Print the received float data
        print(data_float)
    
    except KeyboardInterrupt:
        # Break the loop if Ctrl+C is pressed
        break

# Close the serial connection
ser.close()
