import numpy as np
from PIL import ImageGrab
import gphoto2cffi as gp
from sh import gphoto2 as gp2

from time import sleep
from datetime import datetime
import signal, os, subprocess
import math

import asyncio

import nclib
import haversine as hs
from haversine import Unit

from pymavlink import mavutil

try:
    from dronekit import connect, VehicleMode, Command, LocationGlobal

    Adm_Home=LocationGlobal( 45.404464,-72.144521)
    Adm_1=LocationGlobal( 45.404315,-72.144480, 20)
    Adm_2=LocationGlobal( 45.404257,-72.144408, 20)
    Adm_3=LocationGlobal( 45.404278,-72.144296, 20)
    Adm_4=LocationGlobal( 45.404130,-72.144180, 20)
    Adm_5=LocationGlobal( 45.404485,-72.144404, 20)
    Adm_6=LocationGlobal( 45.404598, -72.144494, 20)
    Adm_7=LocationGlobal(  45.404621, -72.144688, 20)

    targetList = [ Adm_1, Adm_2, Adm_3, Adm_4, Adm_5, Adm_6, Adm_7, Adm_Home] 
    
    #TODO: Implement list retrieval from templated file

except ImportError:
    print("can't import dronekit")

nc = None
dayLake = "BromptonDay5_"
album = []
countPics = 0
pic = ""

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")
num_pics_day = 0

picID = "UbergaiterAcquisition_"
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

def killGphoto2Processes():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:            
            pid = int(line.split(None,1)[0])
            print(pid)
            os.kill(pid, signal.SIGKILL)

async def getVehicleReady(portName):
    vehicle = None
    try:
        vehicle = await connectVehicle(portName)
        vehicle = await armVehicle(vehicle)
        vehicle = await changeVehicleMode('GUIDED')
    except:
        print('Could not get vehicle ready')
    return vehicle

async def connectVehicle(portName):
    try:
        print("trying to connect ....")
        vehicle = connect(portName, wait_ready=True, baud=115200) 
        print("connected to drone through raspberry pi at " + portName)
        print ("Vehicle status:", vehicle.system_status.state)
        return vehicle

    except:
        print('Could not connect drone at ' + portName)
        sys.exit()

async def armVehicle(vehicle):
    if drone_connected == True:
        try: 
            vehicle.armed = True
        except:
            print("can't arm drone")
    return vehicle

async def changeVehicleMode(vehicle, mode):
    try: 
        vehicle.mode = VehicleMode(mode)
        print("Drone has been changed to " + str(mode))
    except:
        print("Drone can't get in " + str(mode) + " mode")
    return vehicle

def connectEmlid():
    try:
        nc = nclib.Netcat(('192.168.2.56', 9001))
        return nc
    except:
        print("could not connect to Emlid")

class PictureMetaData:
    def __init__(self, vehicle):
        self.lat = vehicle.location.global_relative_frame.lat
        self.lon = vehicle.location.global_relative_frame.lon
        self.fix = vehicle.gps_0.fix_type
        self.hdop = vehicle.gps_0.eph  
        self.time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def __str__(self):
        return f"_{str(self.lat)}_{str(self.lon)}_{str(self.fix)}_{str(self.hdop)}_{str(self.time)}_"

async def take_picture(vehicle):
    global countPics
    global my_cam
    pictureName = await createPictureName(vehicle)
    try:
        imgdata = my_cam.capture() 
        with open(pictureName, "wb") as binary_file:
            binary_file.write(imgdata)  
        sleep(1)
        countPics = countPics + 1
        print(f"took {pictureName} in photo")
    except: 
        print(f"Cannot take picture: {pictureName}")

async def getPictureMetaData(vehicle):
    presentPictureMetaData = PictureMetaData(vehicle)   
    return presentPictureMetaData

async def createPictureName(vehicle):
    global save_location
    global countPics
    global dayLake
    global shot_time
    metaDataObject = await getPictureMetaData(vehicle)
    picName = metaDataObject
    picTag = dayLake + shot_time + "picNo_" + str(countPics) + picName + ".png"    
    pictureName = os.path.join(save_location, picTag)
    return pictureName

async def getCamera():
    try:
        my_cam = await gp.Camera()
        return my_cam
    except:
        print("can not get cam")
        sys.exit()

class PresentLocation:
    def __init__(self, vehicle):
        self.lat = vehicle.location.global_relative_frame.lat
        self.lon = vehicle.location.global_relative_frame.lon
        self.location = {"lat":lat,"lon":lon}

    def __str__(self):
        return f"_{str(self.lat)}_{str(self.lon)}_"
    
    def getLocation(self):
        return self.location

async def calculateDistanceToTarget(vehicle, target):
    presentLocation = PresentLocation(vehicle)
    presentCoordinates = (presentLocation.lat, presentLocation.lon)
    targetLocation = (target.lat, target.lon) 
    dist = hs.haversine(targetLocation,presentCoordinates,unit=Unit.METERS)
    print(f"dist = {dist}")
    return distanceToTarget

async def cross_Distance(vehicle, target):   
    print (f"going to : latitude : {target.lat}  longitude: {target.lon}")
    targetLoc = LocationGlobal(target.lat, target.lon, 20)
    try:
        drone.simple_goto(targetLoc)
        distance = 1000
        while distance > 0.2:
            distance = calculateDistanceToTarget(target)
        #await take_picture(vehicle) # surveying phase
        print(f"arrived at {target.name}")
    except:
        print(f"Can not operate simple_goto to {target.name} at {datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")}")

async def run():
    vehicle = getVehicleReady('/dev/ttyACM0')
    my_cam = getCamera()
    nc = connectEmlid()
    killGphoto2Processes()   
    createSaveFolder()
    await asyncio.sleep(5)   
    asyncio.ensure_future(take_picture(vehicle)) #acquisition phase
    for target in targetList:
        await cross_Distance(vehicle, target)
    vehicle.close()
    print(f"mission over with {num_pics_day} pictures taken")

if __name__ == "__main__":   
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    finally:
        loop.close()
