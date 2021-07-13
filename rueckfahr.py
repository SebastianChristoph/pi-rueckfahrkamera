import picamera
import time
import tkinter as tk
from tkinter import font
import datetime
from gpiozero import DistanceSensor
from gpiozero import Buzzer
import MPU6050

camera = picamera.PiCamera()
buz = Buzzer(18) #auf GPIO 21 und GND
HEIGHT = 450
WIDTH = 800
root = tk.Tk()

camAn = 0
sensorVar = DistanceSensor(24, 23) #23 auf trigger, 24 auf echo, mit widerstanden siehe Netz, 5V
abstandAn = 1
gyroAn = 1
gyroNeig_x = 10     #maximale x-Neigung
gyroNeig_x2 = -10   #maximale x-Neigung
gyroNeig_y = 10
gyroNeig_y2 = -10 

mpu = MPU6050.MPU6050() #gyro an SDA1, SCL1, 5V und GND
accel = [0]*3
gyro = [0]*3

def setup():
    mpu.dmp_initialize()
    
def gyro1():
    global accel, gyro, mpu
   
    if gyroAn == 1:
        
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()   
        labelGyro.config(text = "X: %.2f° Y: %.2f° "%(accel[0]/16384.0*90,accel[1]/16384.0*90))
        
        xpruf = accel[0]/16384.0*90
        ypruf = accel[1]/16384.0*90
        
        if xpruf >= gyroNeig_x:
            iconx1.place(x=550, y=300)
            iconx2.place_forget()
            iconx3.place_forget()
        elif xpruf <= gyroNeig_x2:
            iconx2.place(x=550, y=300)
            iconx1.place_forget()
            iconx3.place_forget()
        else:
            iconx3.place(x=550, y=300)
            iconx1.place_forget()
            iconx2.place_forget()
            
        if ypruf >= gyroNeig_y:
            icony1.place(x=675, y=300)
            icony2.place_forget()
            icony3.place_forget()
        elif ypruf <= gyroNeig_y2:
            icony2.place(x=675, y=300)
            icony1.place_forget()
            icony3.place_forget()
        else:
            icony3.place(x=675, y=300)
            icony1.place_forget()
            icony2.place_forget()
        
        
        labelGyro.after(400,gyro1)
        
       
    else:
        labelGyro.config(text = "")


def gyroAus():
    global gyroAn
    
    gyroAn = 0
    print(gyroAn)
    
def gyroEin():
    global gyroAn
    
    gyroAn = 1
    print(gyroAn)

def abstandAus():
    global abstandAn
    
    abstandAn = 0
    print(abstandAn)
    
def abstandEin():
    global abstandAn
    
    abstandAn = 1
    print(abstandAn)
    
def sensor():
    global sensorVar, abstandAn
    
    if abstandAn == 1:
        sensor2 = str(sensorVar.distance*100)
        sensor_beep = sensorVar.distance*100
        sensor3 = sensor2[0:4]
        labelSens.config(text = sensor3 + " cm")
        labelSens.after(450,sensor)
        
        if sensor_beep <= 30:
            buz.on()
            time.sleep(0.1)
            buz.off()
#        elif sensor_beep <= 20:
#            print(sensor_beep)
#            buz.on()

    else:
        labelSens.config(text = "")


def kameraAn():

        print("Live-Vorschau ist an!")
        camera.start_preview(fullscreen=False,window = (2, 50, 540, 405))# position und größe
        camAn = 1
        labelAk(camAn)
        
        #time.sleep(2) #später löschen
        #camera.stop_preview() #später löschen
        
def kameraAus():
        camera.stop_preview()
        print("Live-Vorschau ist aus!")
        camAn = 0
        labelAk(camAn)

def labelAk(camAn):
    print("Der Eintrag ist: ", camAn)
    label["text"] = camAn
    

    
#visuals
canvas = tk.Canvas(root,bg="black", height=HEIGHT, width=WIDTH )
label = tk.Label(root,text = str(camAn), font = ("Modern", 20), bd=4) #Art und Größ
labelSens = tk.Label(root, text = "", bg= "Black", bd=4 , fg="Red", font="Courier 28 bold")
labelGyro = tk.Label(root, text = "", bg="Black", fg="Green",font="Courier 16 bold")

x_lage=tk.PhotoImage(file="iconx2.png")
x_lage2=tk.PhotoImage(file="iconx1.png")
x_lage3=tk.PhotoImage(file="iconx3.png")

iconx1 = tk.Label(root, image=x_lage)
iconx2 = tk.Label(root, image=x_lage2)
iconx3 = tk.Label(root, image=x_lage3)

y_lage=tk.PhotoImage(file="icony2.png")
y_lage2=tk.PhotoImage(file="icony1.png")
y_lage3=tk.PhotoImage(file="icony3.png")

icony1 = tk.Label(root, image=y_lage)
icony2 = tk.Label(root, image=y_lage2)
icony3 = tk.Label(root, image=y_lage3)
canvas.pack()

labelSens.place(x=630, y=160)
labelGyro.place(x=550, y=260)


print("Programm startet")

setup()

gyroEin()
gyro1()
abstandEin()
sensor()
kameraAn()
