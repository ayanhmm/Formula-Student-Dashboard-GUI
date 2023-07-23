import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import serial
import time
import math
import logging


from time import gmtime, strftime
from datetime import datetime
import csv
#----------------------------------------------Configure logging----------------------------------------------
# logging.basicConfig(filename='data.log', level=logging.INFO, format='%(asctime)s %(message)s')
#to conserve primary memory of dashboard screen,data is logged diectly at pit
data_to_append = [['Time','Motor Temperature','Motor Controller Temperature','ERPM','Speed','Throttle','Pack Current','Instantaneous Pack Voltage','State of charge','High Temperarture','Low Temperature','BMS_INPUT_VOL','mc_input_vol','mc_input_current','MC FAULTS','BMS FAULTS']]
# file = open(r"/home/pi/Downloads/datalog/logfile.csv", 'a', newline='')
# writer = csv.writer(file)
# writer.writerows(data_to_append)
# file.close()
file_name = time.ctime()
file_name = file_name + '.csv'
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_to_append)
    file.close()

# ----------------------------------------------Create the root window----------------------------------------------
root = tk.Tk()
#root.title("TDR - SDC")
#root.attributes('-fullscreen', True)

#----------------------------------------------bg of root window----------------------------------------------

# Get the screen width and height
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
# screen_height = int(round((screen_height*2)/7, 0))
# screen_width = int(round((screen_width*5)/15, 0))
#print(screen_width, screen_height)

root.geometry("%dx%d" % (screen_width, screen_height))

#make bg dimentions equal to window
# flash_image = Image.open("flash image 3.png")
# if flash_image.size != (screen_width, screen_height):
#     flash_image = flash_image.resize((screen_width, screen_height), Image.ANTIALIAS)
# flash_image = ImageTk.PhotoImage(flash_image)

#Adding background image in form of a label
#removed since adding blinking caution button is easiar in canvas
# flash_image_label = ttk.Label(root, image = flash_image)
# flash_image_label.place(relx=0, rely=0, anchor="nw")
# flash_image_label.image = flash_image

root.attributes('-fullscreen', True)
# root.after(100)

#----------------------------------------------bg of main canvas window----------------------------------------------
#make bg dimentions equal to window
bg_image_pg1 = Image.open("new dash.png")
if bg_image_pg1.size != (screen_width, screen_height):
    bg_image_pg1 = bg_image_pg1.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image_pg1 = ImageTk.PhotoImage(bg_image_pg1)
#Adding background image in form of a canvas
bg_canvas_pg1 = tk.Canvas(root, width=screen_width, height=screen_height,bg="black")
bg_canvas_pg1.place(relx=1, rely=1, anchor="se")
bg_canvas_pg1.create_image(0, 0, anchor="nw", image=bg_image_pg1)

#----------------------------------------------make canvas for throttle bar----------------------------------------------
throttle_canvas = tk.Canvas(root, width=int(round((screen_width * 27)/36, 0)), height=int(round((screen_height * 1)/20, 0)),bg="black", borderwidth=0, highlightthickness=0)
throttle_canvas.place(relx=1, rely=0.025, anchor="ne")

throttle_canvas_outer_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 4)/36, 0)), 0, int(round((screen_width * 23)/36, 0)), int(round((screen_height * 1)/20, 0)),fill="Orange Red", outline="white",width="2", tags="throttle_outline")
throttle_canvas_inner_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/72, 0)), 0, int(round((screen_width * 45)/72, 0)), int(round((screen_height * 1)/20, 0)),fill="black", outline="white",width="2", tags="throttle_outline")

throttle_bar_outline_rectangle = throttle_canvas.create_rectangle(int(round((screen_width * 9)/38, 0)), int(round((screen_height * 1)/100, 0)), int(round((screen_width * 43)/72, 0)), int(round((screen_height * 8)/200, 0)),fill="black", outline="white",width="1", tags="throttle_outline")

throttle_canvas.create_text(int(round((screen_width * 16)/72, 0)), int(round((screen_height * 1)/68, 0)), text="THROTTLE ::", font=("areal black", int(round((screen_height * 1)/46, 0))), fill="white",anchor="ne" )

def create_gradient_throttle(current, total):
            speedometer_bg_outer_gradient_colour = (255,165,0)    # Start color (red)
            speedometer_bg_inner_gradient_colour = (200,0,0) 
            r1, g1, b1 = speedometer_bg_outer_gradient_colour
            r2, g2, b2 = speedometer_bg_inner_gradient_colour

            r = int(r1 + ((r2-r1) * current/total))
            g = int(g1 + ((g2-g1) * current/total))
            b = int(b1 + ((b2-b1) * current/total))

            return "#%02x%02x%02x" % (r, g, b)
        
for i in range(100):
    gradient_color = create_gradient_throttle(100-i,100)
    throttle_canvas.create_rectangle(int(round((screen_width * 64800)/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * (((100-i)*986)+64800))/273600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill=gradient_color, outline=gradient_color ,width="1", tags="throttle_outline")

#----------------------------------------------CREATE DATA DISPLAY LABELS for circular display----------------------------------------------
#declare font parameters
display_labels_font_style = "RACE SPACE REGULAR"
circular_display_labels_font_color = "Orange Red"
list_display_labels_font_color = "Orange Red"
circular_display_labels_font_size = int(round((screen_width * 1)/45, 0))

# Create label to display pack VOLTAGE
label_data_pack_voltage = tk.Label(bg_canvas_pg1, text="BV", font=(display_labels_font_style,circular_display_labels_font_size ), bg="black", fg=circular_display_labels_font_color)
label_data_pack_voltage.place(relx=0.15, rely=0.2, anchor="center")

# Create label to display ERPM
label_data_ERPM = tk.Label(bg_canvas_pg1, text="AT", font=(display_labels_font_style, circular_display_labels_font_size), bg="black", fg=circular_display_labels_font_color)
label_data_ERPM.place(relx=0.53, rely=0.2, anchor="center")
# Create label to display pack CURRENT
label_data_pack_current = tk.Label(bg_canvas_pg1, text="BC", font=(display_labels_font_style, circular_display_labels_font_size), bg="black", fg=circular_display_labels_font_color)
label_data_pack_current.place(relx=0.35, rely=0.2, anchor="center")

# Create label to display MOTOR TEMP
label_data_motor_temperature = tk.Label(bg_canvas_pg1, text="MT", font=(display_labels_font_style, circular_display_labels_font_size), bg="black", fg=circular_display_labels_font_color)
label_data_motor_temperature.place(relx=0.88, rely=0.2, anchor="center")
# Create label to display MOTOR controller TEMP
label_data_motor_controller_temperature = tk.Label(bg_canvas_pg1, text="MCT", font=(display_labels_font_style, circular_display_labels_font_size), bg="black", fg=circular_display_labels_font_color)
label_data_motor_controller_temperature.place(relx=0.72, rely=0.2, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for list display on left side----------------------------------------------
# Create label to display charge
label_data_charge = tk.Label(bg_canvas_pg1, text="BP", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_charge.place(relx=0.23, rely=0.490, anchor="center")
# Create label to display battery_max_temperature
label_data_battery_max_temperature = tk.Label(bg_canvas_pg1, text="FS", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_max_temperature.place(relx=0.372, rely=0.57, anchor="center")

# Create label to display mfr
label_data_bps = tk.Label(bg_canvas_pg1, text="LVBS", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bps.place(relx=0.23, rely=0.420, anchor="center")
# Create label to display battery_min_temperature
label_data_battery_min_temperature = tk.Label(bg_canvas_pg1, text="TMT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_battery_min_temperature.place(relx=0.383, rely=0.63, anchor="center")
# # Create label to display MFR -- NOT REQUIRED TO DISPLAY  
# label_data_MFR = tk.Label(bg_canvas_pg1, text="TMT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
# label_data_MFR.place(relx=0.71, rely=0.420, anchor="center")  

#----------------------------------------------CREATE DATA DISPLAY LABELS for list display on right side----------------------------------------------
# Create label to MC input voltage
label_data_MC_input_voltage = tk.Label(bg_canvas_pg1, text="MCIV", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_MC_input_voltage.place(relx=0.8, rely=0.420, anchor="center")
# Create label to MC input charge
label_data_MC_input_charge = tk.Label(bg_canvas_pg1, text="MCIC", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_MC_input_charge.place(relx=0.8, rely=0.490, anchor="center")
# Create label to MC input charge
label_data_LV_battery_voltage = tk.Label(bg_canvas_pg1, text="LVBV", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_LV_battery_voltage.place(relx=0.815, rely=0.562, anchor="center")


#----------------------------------------------CREATE RPM and speed DISPLAY LABELS----------------------------------------------
#become obsolete after addition of speedometer and rpm dial
# Create label to display RPM
# label_data_rpm = tk.Label(bg_canvas_pg1, text="RPM", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
# label_data_rpm.place(relx=0.67, rely=0.775, anchor="center")
# Create label to display speed
label_data_speed = tk.Label(bg_canvas_pg1, text="SPD", font=(display_labels_font_style,int(round((screen_width * 1)/20, 0))), bg="black", fg=list_display_labels_font_color)
label_data_speed.place(relx=0.72, rely=0.8, anchor="center")

#----------------------------------------------CREATE DATA DISPLAY LABELS for throttle canvas----------------------------------------------
label_data_throttle = tk.Label(throttle_canvas, text="tht", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_throttle.place(relx=0.1, rely=0.5, anchor="center")

#----------------------------------------------CREATE Fault DISPLAY LABELS----------------------------------------------
# Create label to display MOTOR controller faults
label_data_motor_controller_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_motor_controller_fault.place(relx=0.14, rely=0.82, anchor="center")
# Create label to display bms faults
label_data_bms_fault = tk.Label(bg_canvas_pg1, text="FAULT", font=(display_labels_font_style, int(round((screen_width * 1)/60, 0))), bg="black", fg=list_display_labels_font_color)
label_data_bms_fault.place(relx=0.34, rely=0.82, anchor="center")

#----------------------------------------------Open serial connection to Arduino----------------------------------------------
#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/ttyACM0',460800)

#----------------------------------------------data updation on main window----------------------------------------------
def update_data():
    #obtain raw data from arduino
    raw_data  = ser.readline()
    try:
        raw_data = raw_data.decode()
        data = raw_data.split("\"")
    # Process the decoded data here
    except UnicodeDecodeError:
    # Handle the case when the data cannot be decoded
        root.after(1, update_data)
    #raw_data = '000,100,2000,30,40.00,500,600,700,800,900,1000,110,120,no mc fault a :no mc fault b:no mc fault c:no mc fault d; no bms fault a : no bms fault b: no bms fault c: no bms fault d'
    #print(raw_data)
    #split raw data into list of datas from different sensor

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
    if len(data) >= 14:
        #----------------------------------------------data loggging----------------------------------------------
        file = open(file_name, 'a', newline='')
        writer = csv.writer(file)
        data_to_append = []
        datalist0 = data
        print(datalist0)
        if len(datalist0) == 14:
            datalist1 = datalist0[13].split(";")
            finaldatalist = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            for i in range(13):
                finaldatalist.append(datalist0[i])
            finaldatalist.append(datalist1[0])
            finaldatalist.append(datalist1[1])
            data_to_append.append(finaldatalist)
                
            writer.writerows(data_to_append)
        file.close()


        #----------------------------------------------display values update----------------------------------------------
        label_data_motor_temperature.config(text = data[0])
        label_data_motor_controller_temperature.config(text = data[1])
        # label_data_rpm.config(text = data[2])
        label_data_ERPM.config(text = data[2])
        label_data_pack_current.config(text = data[5]) 
        label_data_pack_voltage.config(text = data[6]) 
        label_data_charge.config(text = data[7])        
        label_data_battery_max_temperature.config(text = data[8])
        label_data_battery_min_temperature.config(text = data[9])
        # label_data_bps.config(text = data[10])
        label_data_MC_input_voltage.config(text = data[11])
        label_data_MC_input_charge.config(text = data[12])
        label_data_LV_battery_voltage.config(text = data[10])
        #label_data_MFR.config(text = data[10])
        
        #label_data_speed.config(text = current_vehicle_calculated_speed)
        label_data_speed.config(text = data[3])
        
        label_data_throttle.config(text = data[4])
        #----------------------------------------------display faults update----------------------------------------------
        label_data_motor_controller_fault.config(text = mc_faults_string_arranged)
        #label_data_bms_fault.config(text = bms_faults_string_arranged)
        
        def update_throttle_bar():
            throttle_canvas.delete("throttle_black_fill")
            throttle_percentage = int(float(data[4]))
            throttle_canvas.create_rectangle(int(round((screen_width * (((throttle_percentage)*986)+64800))/273600, 0))+1, int(round((screen_height * 2)/200, 0))+1, int(round((screen_width * ((100*986)+64800))/273600, 0))-1, int(round((screen_height * 1)/25, 0))-1,fill="black", outline="",width="1", tags="throttle_black_fill")
        
        update_throttle_bar()

    
    #----------------------------------------------repead the update data function after 100ms----------------------------------------------   
    root.after(1, update_data) 
    # start_time = time.time()
    # while (time.time() - start_time) < 0.0005:
    #     update_data()

#----------------------------------------------start data updation on main window----------------------------------------------
root.after(1, update_data) 
#update_data()
    
root.mainloop()