# Formula Student Dashboard GUI
 GUI to display the data obtained from various sensors on the dashboard of the car as well as log it for future references

## pre requirements::

(1)TKINTER - pip install tk

(2)PIL - pip install pillow

(3)serial - pip install pyserial


## requirements no longer required in latest version 
=>PANDAS - pip install pandas , pip install openpyxl

=> Read arduino data -   pip install p
                         pip install pyserial pySerialTransfer
                         
                         
## install fonts- 
https://fontmeme.com/polices/police-caution/
https://fontmeme.com/polices/police-racing-numbers/#previewtool
https://fontmeme.com/polices/police-race-space/


## sources of errors::
Utf decode - baud rate of arduino and ui code SER.read should be same
             fixed by adding condition to decode only if decoding can be done

Can bus fail - mcp to arduino connections loose
               fixed by tightning wire connections

Port busy- ide running in background, 
           fix by closing it’s serial moniter 

Arduino not detected - wrong port name declared in ui ser.read

Data not refreshing in gui - data list recieved from arduino is shorter than the data being displayed in the ui

Resizing error - fixed :: donot resize in code but resize before hand using google. This will also conserve primary memory

Delayed data - reduce delay in root.after(). this delay should be equal to the delay in arduino code
