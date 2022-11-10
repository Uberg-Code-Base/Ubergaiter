import numpy as np
import serial
import pynmea2
import string
from PIL import ImageGrab
import asyncio
import nclib

nc = None
port = '/dev/serial0'
ser = serial.Serial(port,baudrate=9600,timeout=0.5)
dataout = pynmea2.NMEAStreamReader()



from pymavlink import mavutil
import gphoto2cffi as gp
try:
    from dronekit import connect, VehicleMode, Command, LocationGlobal
   
    Adm_12=LocationGlobal( 45.404494, -72.144429, 20)

except ImportError:
    print("can't import dronekit")
import haversine as hs
from haversine import Unit
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp2
import signal, os, subprocess
import math

dayLake = "Beauchamp_Day17_"
album = []
pic = ""
vehicle = None
drone_connected = False
lat = 0.0
lon = 0.0
fix = 0
hdop = 0
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
num_pics_day = 0
countPics = 0
x=""
y=""
z=""
ns=""
cmPrecision = ""
time = ""

def connectEmlid():
    try:
        newdata = ser.readline().decode()
        if newdata[0:6]=="$GPRMC":
            print("connected to reach")
        if newdata.lat == '':
            print('no gps data')
        else:
            print('gps data obtained')       
    except:
        print("could not connect to Emlid")

def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()  
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:          
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
        if b'gvfs-gphoto2-volume-monitor' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

killGphoto2Process()
my_cam = gp.Camera()
connectEmlid()

picID = "_UbergaiterAcquisition_"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
timeCommand = ["--set-config datetime=$(date +%s)"]

folder_name = dayLake + picID
save_location = "/home/uberg/Documents/gphoto/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)
   
async def armDrone():
    if drone_connected == True:
        try: 
                vehicle.armed = True
                if vehicle.armed == True:
                        vehicle.mode = VehicleMode("GUIDED") 
                        if vehicle.mode.name == "GUIDED":
                                print ("drone is armed and ready in GUIDED mode")
                                
                                return vehicle
                        else: print("drone can't get in GUIDED mode")
                else: print("drone can't arm")
        except:
                print("can't arm drone")
      
async def cross_Distance(target, vehicle): 
    print (f"going to : latitude : {target.lat}  longitude: {target.lon}")
    dist = 1000.0
    lat = target.lat
    lon = target.lon
    targetLoc = LocationGlobal(lat,lon,20)
    drone = vehicle
    drone.simple_goto(targetLoc)

    while dist > 0.2:
        locA = (lat, lon) 
        locBlat = 0.0
        locBlon = 0.0
        currentLocation = vehicle.location.global_relative_frame
        locBlat = currentLocation.lat
        locBlon = currentLocation.lon
        gpsInfo = vehicle.gps_0
        fix = gpsInfo.fix_type
        hdop = gpsInfo.eph
        dist = hs.haversine(locA,(locBlat, locBlon),unit=Unit.METERS)
        print(f"dist = {dist}")       
        response = nc.recv()
        sentence = response.split()
        x=str(sentence[2],'utf-8')
        y=str(sentence[3],'utf-8')
        z=str(sentence[4],'utf-8')
        time=str(sentence[1],'utf-8')
        ns=str(sentence[6],'utf-8')
        sdn=float(str(sentence[7],'utf-8'))
        sde=float(str(sentence[8],'utf-8'))
        cmPrecision=str(math.sqrt(math.pow(sdn,2)+math.pow(sde,2)))
        
        await take_screen(lat,lon,fix,hdop, x,y,z,ns,cmPrecision, time)
    print(f"arrived at {target.name}")

async def connectDrone(): 
    print("trying to connect ....")
    vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=115200) 
    print("connected to drone through raspberry pi")
    print ("Vehicle status:", vehicle.system_status.state)
    drone_connected = True
    if drone_connected == True:
        try: 
                vehicle.armed = True
                if vehicle.armed == True:
                        vehicle.mode = VehicleMode("GUIDED") 
                        if vehicle.mode.name == "GUIDED":
                                print ("drone is armed and ready in GUIDED mode")
                                return vehicle
                        else: 
                            print("drone can't get in GUIDED mode")
                            return vehicle
                else: print("drone can't arm")
        except:
                print("can't arm drone")

async def take_screen(lat,lon,fix,hdop, x,y,z,ns,cmPrecision, time):
    global save_location
    global countPics
    global dayLake
   
    picReach=""
    try:    
        for i in range(10):
            try:
                newGPSLine = ser.readline().decode('ascii', errors='replace')
                newGPS = pynmea2.parse(newGPSLine)
                print(newGPS.latitude)
                picReach = "_M" + str(newGPS.latitude) + "_N" + str(newGPS.longitude) + "_T" + str(newGPS.timestamp)
                break
            except: print()
            
    except:
        picReach = ""

    picTag = dayLake + shot_time + "picNo_" + str(countPics) + picReach + ".png"
    completeName = os.path.join(save_location, picTag)
    imgdata = my_cam.capture() 
    with open(completeName, "wb") as binary_file:
        binary_file.write(imgdata)      
    sleep(1)
    countPics = countPics + 1
    print(f"took {picTag} in picture")

async def run():
    print("connected, continuing process")
    killGphoto2Process()
    createSaveFolder()
    await asyncio.sleep(5) 
    timer = 0
    while(timer < 10000):
        await take_screen(lat,lon,fix,hdop,x,y,z,ns,cmPrecision,time)
        timer = timer+1    
    print(f"mission over with {num_pics_day} pictures taken")
 
if __name__ == "__main__":  
    asyncio.ensure_future(run())   
    asyncio.get_event_loop().run_forever()