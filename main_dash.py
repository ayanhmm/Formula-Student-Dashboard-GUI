import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import time
import math
import logging
#----------------------------------------------Configure logging----------------------------------------------
logging.basicConfig(filename='data.log', level=logging.INFO, format='%(asctime)s %(message)s')

# ----------------------------------------------Create the root window----------------------------------------------
root = tk.Tk()
root.title("TDR - SDC")

#----------------------------------------------bg of root window----------------------------------------------
# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
print(screen_width, screen_height)
screen_width = screen_width - 20
screen_height = screen_height -70
root.geometry("%dx%d" % (screen_width, screen_height))
#make bg dimentions equal to window
bg_image_pg1 = Image.open("new dash.png")
if bg_image_pg1.size != (screen_width, screen_height):
    bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.ANTIALIAS)
bg_image_pg1 = ImageTk.PhotoImage(bg_image_pg1)
#Adding background image in form of a label
bg_label_pg1 = ttk.Label(root, image = bg_image_pg1)
bg_label_pg1.place(relx=0.5, rely=0.5, anchor="center")
bg_label_pg1.image = bg_image_pg1

#----------------------------------------------CREATE DATA DISPLAY LABELS----------------------------------------------
# Create label to display BATTERY VOLTAGE
label_data_pack_voltage = tk.Label(root, text="BV", font=("Arial black", 10), bg="black", fg="red")
label_data_pack_voltage.place(relx=0.13, rely=0.18, anchor="center")
# Create label to display ACCUMULATOR TEMPERATURE
label_data_throttle = tk.Label(root, text="AT", font=("Arial black", 10), bg="black", fg="red")
label_data_throttle.place(relx=0.4, rely=0.18, anchor="center")
# Create label to display BATTERY CURRENT
label_data_pack_current = tk.Label(root, text="BC", font=("Arial black", 10), bg="black", fg="red")
label_data_pack_current.place(relx=0.66, rely=0.18, anchor="center")
# Create label to display RPM
label_data_rpm = tk.Label(root, text="RPM", font=("Arial black", 15), bg="black", fg="red")
label_data_rpm.place(relx=0.62, rely=0.72, anchor="center")
# Create label to display speed
label_data_speed = tk.Label(root, text="SPD", font=("Arial black", 20), bg="black", fg="red")
label_data_speed.place(relx=0.83, rely=0.66, anchor="center")
# Create label to display brake pressure
label_data_charge = tk.Label(root, text="BP", font=("Arial black", 10), bg="black", fg="red")
label_data_charge.place(relx=0.46, rely=0.794, anchor="center")
# Create label to display fluid speed
label_data_battery_max_temperature = tk.Label(root, text="FS", font=("Arial black", 10), bg="black", fg="red")
label_data_battery_max_temperature.place(relx=0.385, rely=0.89, anchor="center")
# Create label to display MOTOR TEMP
label_data_motor_temperature = tk.Label(root, text="MT", font=("Arial black", 10), bg="black", fg="red")
label_data_motor_temperature.place(relx=0.24, rely=0.46, anchor="center")
# Create label to display MOTOR controller TEMP
label_data_motor_controller_temperature = tk.Label(root, text="MCT", font=("Arial black", 10), bg="black", fg="red")
label_data_motor_controller_temperature.place(relx=0.54, rely=0.46, anchor="center")
# Create label to display lv battery status
label_data_mfr = tk.Label(root, text="LVBS", font=("Arial black", 10), bg="black", fg="red")
label_data_mfr.place(relx=0.48, rely=0.71, anchor="center")
# Create label to display THERMISTOR MAX TEMP
label_data_battery_min_temperature = tk.Label(root, text="TMT", font=("Arial black", 10), bg="black", fg="red")
label_data_battery_min_temperature.place(relx=0.55, rely=0.975, anchor="center")
# Create label to display BPS
label_data_bps = tk.Label(root, text="TMT", font=("Arial black", 10), bg="black", fg="red")
label_data_bps.place(relx=0.55, rely=0.975, anchor="center")  

#----------------------------------------------CREATE Fault DISPLAY LABELS----------------------------------------------
# Create label to display MOTOR controller faults
label_data_motor_controller_fault = tk.Label(root, text="FAULT", font=("Arial black", 10), bg="black", fg="red")
label_data_motor_controller_fault.place(relx=0.54, rely=0.46, anchor="center")
# Create label to display bms faults
label_data_bms_fault = tk.Label(root, text="FAULT", font=("Arial black", 10), bg="black", fg="red")
label_data_bms_fault.place(relx=0.54, rely=0.46, anchor="center")

#----------------------------------------------Open serial connection to Arduino----------------------------------------------
#ser = serial.Serial('/dev/ttyUSB0', 9600)

#----------------------------------------------data updation on main window----------------------------------------------
def update_data():
    #obtain raw data from arduino
    #raw_data  = ser.readline().decode()
    raw_data = '0,1,2,3,4,5,6,7,8,9,10,no mc fault; no bms fault a : no bms fault b'
    
    #split raw data into list of datas from different sensors
    data = raw_data.split(",")
    fault_list = data[-1].split(";")
    
    #calculate speed using erpm and radius of tyres
    erpm = int(data[2])
    tyre_radius = 1
    tyre_circumference = 2*3.14*tyre_radius
    current_vehicle_calculated_speed = ((erpm/10)*tyre_circumference*60)
    current_vehicle_calculated_speed = int(round(current_vehicle_calculated_speed, 0))
    
    #prevent decoding error when "connection with arduino established" is the data recieved from arduino
    if len(data) == 12:
        #----------------------------------------------data loggging----------------------------------------------
        data_to_be_logged = f"\nmotor_temperature: {data[0]},motor_controller_temperature: {data[1]},rpm: {data[2]},throttle: {data[3]},\npack_current: {data[4]},pack_voltage: {data[5]},charge: {data[6]},\nbattery_max_temperature: {data[7]},label_data_battery_min_temperature: {data[8]},\nmfr: {data[9]},bps: {data[10]},speed: {current_vehicle_calculated_speed},\nmc_faults: {fault_list[0]},\nbms_faults: {fault_list[1]}\n"
        logging.info(data_to_be_logged)
        logging.info(current_vehicle_calculated_speed)
        
        #----------------------------------------------display values update----------------------------------------------
        label_data_motor_temperature.config(text = data[0])
        label_data_motor_controller_temperature.config(text = data[1])
        label_data_rpm.config(text = data[2])
        label_data_throttle.config(text = data[3])
        label_data_pack_current.config(text = data[4]) 
        label_data_pack_voltage.config(text = data[5]) 
        label_data_charge.config(text = data[6])        
        label_data_battery_max_temperature.config(text = data[7])
        label_data_battery_min_temperature.config(text = data[8])
        label_data_mfr.config(text = data[9])
        label_data_bps.config(text = data[10])
        
        label_data_speed.config(text = current_vehicle_calculated_speed)
        
        #----------------------------------------------display faults update----------------------------------------------
        label_data_motor_controller_fault.config(text = fault_list[0])
        label_data_bms_fault.config(text = fault_list[1])

        #----------------------------------------------repead the update data function after 100ms----------------------------------------------
        root.after(100, update_data) 

#----------------------------------------------start data updation on main window----------------------------------------------
update_data()

root.mainloop()