import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import time
import math
import logging
#----------------------------------------------Configure logging----------------------------------------------
# logging.basicConfig(filename='data.log', level=logging.INFO, format='%(asctime)s %(message)s')
#to conserve primary memory of dashboard screen,data is logged diectly at pit

# ----------------------------------------------Create the root window----------------------------------------------
root = tk.Tk()
#root.title("TDR - SDC")
#root.attributes('-fullscreen', True)

#----------------------------------------------bg of root window----------------------------------------------

# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# screen_height = int(round((screen_height*2)/7, 0))
# screen_width = int(round((screen_width*5)/15, 0))
print(screen_width, screen_height)

root.geometry("%dx%d" % (screen_width, screen_height))


#make bg dimentions equal to window
bg_image_pg1 = Image.open("new dash.png")
if bg_image_pg1.size != (screen_width, screen_height):
    bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.ANTIALIAS)
bg_image_pg1 = ImageTk.PhotoImage(bg_image_pg1)

##Adding background image in form of a label
##removed since adding blinking caution button is easiar in canvas
# bg_label_pg1 = ttk.Label(root, image = bg_image_pg1)
# bg_label_pg1.place(relx=0, rely=0, anchor="nw")
# bg_label_pg1.image = bg_image_pg1

#Adding background image in form of a canvas
bg_canvas_pg1 = tk.Canvas(root, width=screen_width, height=screen_height,bg="red")
bg_canvas_pg1.place(relx=0, rely=0, anchor="nw")
bg_canvas_pg1.create_image(0, 0, anchor="nw", image=bg_image_pg1)

root.attributes('-fullscreen', True)

#----------------------------------------------CREATE DATA DISPLAY LABELS for circular display----------------------------------------------
# Create label to display pack VOLTAGE
display_labels_font_style = "RACE SPACE REGULAR"
circular_display_labels_font_color = "Orange Red"
list_display_labels_font_color = "Orange Red"

label_data_pack_voltage = tk.Label(bg_canvas_pg1, text="BV", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_pack_voltage.place(relx=0.15, rely=0.2, anchor="center")

# Create label to display throttle
label_data_throttle = tk.Label(bg_canvas_pg1, text="AT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_throttle.place(relx=0.55, rely=0.2, anchor="center")
# Create label to display pack CURRENT
label_data_pack_current = tk.Label(bg_canvas_pg1, text="BC", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_pack_current.place(relx=0.35, rely=0.2, anchor="center")

# Create label to display MOTOR TEMP
label_data_motor_temperature = tk.Label(bg_canvas_pg1, text="MT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_motor_temperature.place(relx=0.88, rely=0.2, anchor="center")
# Create label to display MOTOR controller TEMP
label_data_motor_controller_temperature = tk.Label(bg_canvas_pg1, text="MCT", font=(display_labels_font_style, int(round((screen_width * 1)/45, 0))), bg="black", fg=circular_display_labels_font_color)
label_data_motor_controller_temperature.place(relx=0.72, rely=0.2, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for list display----------------------------------------------
# Create label to display charge
label_data_charge = tk.Label(bg_canvas_pg1, text="BP", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_charge.place(relx=0.27, rely=0.490, anchor="center")
# Create label to display battery_max_temperature
label_data_battery_max_temperature = tk.Label(bg_canvas_pg1, text="FS", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_max_temperature.place(relx=0.369, rely=0.57, anchor="center")

# Create label to display mfr
label_data_mfr = tk.Label(bg_canvas_pg1, text="LVBS", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_mfr.place(relx=0.22, rely=0.420, anchor="center")
# Create label to display battery_min_temperature
label_data_battery_min_temperature = tk.Label(bg_canvas_pg1, text="TMT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_min_temperature.place(relx=0.38, rely=0.63, anchor="center")
# Create label to display BPS
label_data_bps = tk.Label(bg_canvas_pg1, text="TMT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bps.place(relx=0.71, rely=0.420, anchor="center")  

#----------------------------------------------CREATE RPM and speed DISPLAY LABELS----------------------------------------------
#become obsolete after addition of speedometer and rpm dial
# Create label to display RPM
label_data_rpm = tk.Label(bg_canvas_pg1, text="RPM", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_rpm.place(relx=0.67, rely=0.775, anchor="center")
# Create label to display speed
label_data_speed = tk.Label(bg_canvas_pg1, text="SPD", font=(display_labels_font_style,int(round((screen_width * 1)/20, 0))), bg="black", fg=list_display_labels_font_color)
label_data_speed.place(relx=0.83, rely=0.74, anchor="center")
#----------------------------------------------CREATE Fault DISPLAY LABELS----------------------------------------------
# Create label to display MOTOR controller faults
label_data_motor_controller_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_motor_controller_fault.place(relx=0.14, rely=0.82, anchor="center")
# Create label to display bms faults
label_data_bms_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bms_fault.place(relx=0.34, rely=0.82, anchor="center")

#----------------------------------------------Open serial connection to Arduino----------------------------------------------
ser = serial.Serial('/dev/ttyACM0', 9600)

#----------------------------------------------data updation on main window----------------------------------------------
def update_data():
    #obtain raw data from arduino
    raw_data  = ser.readline().decode()
    #raw_data = '0,1,2,3,4,5,6,7,8,9,10,no mc fault a :no mc fault b:no mc fault c:no mc fault d; no bms fault a : no bms fault b: no bms fault c: no bms fault d'
    
    #split raw data into list of datas from different sensors
    data = raw_data.split(",")
    fault_list = data[-1].split(";")
    
    #converting faults to a more organised form
    fault_list = data[-1].split(";")
    bms_faults_string_list = fault_list[-1].split(";")
    bms_faults_list = bms_faults_string_list[0].split(":")
    bms_faults_string_arranged = '\n'.join(bms_faults_list)
    
    mc_faults_string_list = fault_list[0].split(";")
    mc_faults_list = mc_faults_string_list[0].split(":")
    mc_faults_string_arranged = '\n'.join(mc_faults_list)
    

    
    #prevent decoding error when "connection with arduino established" is the data recieved from arduino
    if len(data) <= 10:
        #----------------------------------------------data loggging----------------------------------------------
        # data_to_be_logged = f"\nmotor_temperature: {data[0]},motor_controller_temperature: {data[1]},rpm: {data[2]},throttle: {data[3]},\npack_current: {data[4]},pack_voltage: {data[5]},charge: {data[6]},\nbattery_max_temperature: {data[7]},label_data_battery_min_temperature: {data[8]},\nmfr: {data[9]},bps: {data[10]},speed: {current_vehicle_calculated_speed},\nmc_faults: {fault_list[0]},\nbms_faults: {fault_list[1]}\n"
        # logging.info(data_to_be_logged)
        # logging.info(current_vehicle_calculated_speed)
        # data logged directly at pit
        
        #calculate speed using erpm and radius of tyres
        erpm = int(data[2])
        tyre_radius = 1
        tyre_circumference = 2*3.14*tyre_radius
        current_vehicle_calculated_speed = ((erpm/10)*tyre_circumference*60)
        current_vehicle_calculated_speed = int(round(current_vehicle_calculated_speed, 0))
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
        label_data_motor_controller_fault.config(text = mc_faults_string_arranged)
        label_data_bms_fault.config(text = bms_faults_string_arranged)

        #----------------------------------------------repead the update data function after 100ms----------------------------------------------
        root.after(100, update_data) 

#----------------------------------------------start data updation on main window----------------------------------------------
update_data()

root.mainloop()