import numpy as np
from PIL import ImageGrab
import asyncio
import nclib
from pymavlink import mavutil
import gphoto2cffi as gp
import os
from twilio.rest import Client
from dronekit import connect, VehicleMode, Command, LocationGlobal
import haversine as hs
from haversine import Unit
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp2
import signal, os, subprocess
import math
nc = None

account_sid = '__'
auth_token = '__'
client = Client(account_sid, auth_token)

vehicle = None
drone_connected = False
lat = 0.0
lon = 0.0
fix = 0
hdop = 0
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
num_pics_day = 0
x=""
y=""
z=""
ns=""
cmPrecision = ""
time = ""
my_cam = None
cam_connected = False
cam_alert = False
mission_over = False
num_pics_day = 0

def connectCam():
    try:
        killGphoto2Process()
        cam = gp.Camera()
        return cam
    except:
        print("Cannot connect to camera")

def connectEmlid():
    try:
        nc = nclib.Netcat(('192.168.2.56', 9001))
        return nc
    except:
        print("could not connect to Emlid")

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
                            print ("Vehicle status:", vehicle.system_status.state)
                            print ("drone is armed and ready in GUIDED mode")
                            return vehicle
                    else: 
                        print("drone can't get in GUIDED mode")
                        return vehicle
            else: print("drone can't arm")
        except:
                print("can't arm drone")
    else: 
        print("cannot connect to drone")


def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
        if b'gvfsd-gphoto2' in line:
            b'gvfs-gphoto2-volume-monitor'
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

nc = connectEmlid()
picID = "Ubergaiter_Acquisition_"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
timeCommand = ["--set-config datetime=$(date +%s)"]

folder_name = shot_date + picID
save_location = "/media/uberg/photos/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)

def vehicleDisable():
    vehicle.close()
    print("vehicle closed")
    
async def cross_Distance(target, vehicle, my_cam):
    
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
        await take_screen(my_cam,lat,lon,fix,hdop, x,y,z,ns,cmPrecision, time, num_pics_day)
    print(f"arrived at {target.name}")

async def take_screen(my_cam,lat, lon, fix, hdop, x, y, z, ns, cmPrecision, time, num_pics_day):
    try:   
        killGphoto2Process()
        picName = str(lat) + "-" + str(lon) + "-" + str(fix) + "-" + str(hdop) + "-" + str(x) + "-" + str(y) + "-" + str(z) + "-" + str(ns) + "-" + str(cmPrecision) + "-" + str(time)
        shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
        picTag = shot_time + picName + ".jpg"
        completeName = os.path.join(save_location, picTag)
        imgdata = my_cam.capture() 
        with open(completeName, "wb") as binary_file:
            binary_file.write(imgdata)
        sleep(2)
        num_pics_day = num_pics_day + 1
        shot_time = ""
        print(f"took {picTag} in picture")
    except:
        print("could not take picture") 
        try:
            textMsg = f"Taking pictures did not work. Sorry. At lat:{lat} long:{lon}" 
            if not cam_alert:
                message = client.messages.create(
                                body=textMsg,
                                from_='+18193039366',
                                to='+12502681200',
                                
                          )
                cam_alert = True
        except: print("could not take pics and warn you by text")

async def run():
    import gphoto2cffi as gp
    drone_connected = False
    import sys
    mission_over = False 
    killGphoto2Process()
    my_cam = gp.Camera()
    cam_connected = True
    while cam_connected:
        vehicle = await connectDrone()
        drone_connected = True
        if drone_connected:
            print("connected, continuing process")          
            createSaveFolder()
            a = LocationGlobal(45.404395, -72.143708, 20)
            b = LocationGlobal(45.405081, -72.143752, 20)
            c = LocationGlobal(45.413699, -72.143969, 20)
            d = LocationGlobal(45.416463, -72.139731, 20)
            e = LocationGlobal(45.426051, -72.147345, 20)
            f = LocationGlobal(45.433061, -72.151400, 20)
            g = LocationGlobal(45.404395, -72.143708, 20)
            h = LocationGlobal(45.405081, -72.143752, 20)
            await asyncio.sleep(5)             
            asyncio.ensure_future(take_screen(my_cam,lat,lon,fix,hdop,x,y,z,ns,cmPrecision,time, num_pics_day))
            await cross_Distance(my_cam, a, vehicle)
            await cross_Distance(my_cam, b, vehicle)
            await cross_Distance(my_cam, c, vehicle)
            await cross_Distance(my_cam, d, vehicle)
            await cross_Distance(my_cam, e, vehicle)
            await cross_Distance(my_cam, f, vehicle)
            await cross_Distance(my_cam, h, vehicle)
            vehicle.close()
            print(f"mission over with {num_pics_day} pictures taken")
            mission_over = True
            break
        else: break
    
    if mission_over:
        print("Mission success")
    else: 
        print("cannot connect cam, aborting")
        sys.exit(0)

if __name__ == "__main__":    
    try:
        asyncio.ensure_future(run())       
        asyncio.get_event_loop().run_forever()
        if KeyboardInterrupt:
            try:
                vehicleDisable()
                asyncio.get_event_loop().stop()
                print('Interrupted')
                sys.exit(0)
            except SystemExit:
                os._exit(0)
    except:
        print("exception caught")
        vehicleDisable()
