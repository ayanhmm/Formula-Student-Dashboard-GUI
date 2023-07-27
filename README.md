# Formula Student Dashboard GUI
 GUI to display the data obtained from various sensors on the dashboard of the car as well as log it for future references

## Pre Requirements::

### Install the following python libraries:
1. Tkinter : **```pip install tk```**
2. Python Imaging Library :  **```pip install pillow```**
3. Serial : **```pip install pyserial```**


### Libraries no Longer Required in the Latest Version 
1. **```pip install pandas```**
2. **```pip install openpyxl```**
3. **```pip install p```**
4. **```pip install pyserial pySerialTransfer```**
                         
                         
### Install the following Fonts:
For convenience purposes, downloadable files of the specified fonts have been added to the repository
1. Caution: https://fontmeme.com/polices/police-caution/
2. Race Numbers: https://fontmeme.com/polices/police-racing-numbers/#previewtool
3. Race Space: https://fontmeme.com/polices/police-race-space/


## Sources of Errors:
This is a list of some errors that were faced during implementation of the python UI code while recieving data from the arduino

1. **Utf Decoding Error**- Baud rate of arduino and ui code SER.read should be same.if errer still persists,then can fixed by adding condition to decode only if decoding can be done(see main_dash.py).
2. **Canbus Fail** - Mcp to canbus or mcp to arduino connections are loose and can be fixed by tightning the hardware connections
3. **Port Busy**- Some other application is utilizing the port.it is probably the arduino ide running in background,can be fixed by closing it’s serial moniter.The error still might persist when no application seems to be using specified port, then try restaring your laptop.
4. **Arduino not detected** - wrong port name declared in ui ser.read(see main_dash.py).
5. **Data not refreshing in gui** - data list recieved from arduino is shorter than the data being displayed in the ui(see main_dash.py).This can also happen if there is loosening of the mcp to arduino connections due to which data is no longer being recieved.
6. **Resizing error** - this error sometimes appears while running the code on raspberry pi even if it works effortlessly on laptops. remedy :: donot resize in code but resize before hand using google. This will also conserve primary memory.For the sake of convenience, an image of the same size as our UI screen has been added to the repository
7. **Delayed refreshing** - Some delay might be seen between the sensors sending the data and it being displayed on the UI.
   1. **Baudrate out of sync**: This can also happen if the baudrate by which the sensors specially the motor controller or the bms are sending their data is different from the baudrate by which the arduino or the UI is recieving that data
   2. **Delay Error**: This can be caused if the delay set in the main_dash.py code is too long. this can be easily fixed by reducing the delay in root.after(). this delay should be equal to the delay in arduino code.


## Data Displayed:
The following data is being displayed on the dashboard screen.It is to be notes that the data must also be recieved from the arduino in form of a string separated by comas and in the same order as written below.
1. Motor Temperature
2. Motor Controller Temperature
3. ERPM
4. Speed
5. Throttle
6. Pack Current
7. Instantaneous Pack Voltage
8. State of charge
9. Battery Maximum Temperarture
10. Battery Minimum Temperarture
11. BMS Input Voltage(LV Battery Voltage)
12. Motor Controller Input Voltage
13. Motor Controller Input Current
14. Motor Controller FAULTS
15. BMS FAULTS
<img src="./resources/readme images/working ui.png" alt="UI display" />
