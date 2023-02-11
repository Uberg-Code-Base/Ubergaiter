#!/usr/bin/env python3
import numpy as np
#import cv2
from PIL import ImageGrab
import asyncio
import nclib
nc = None
#import geolib
#from mavsdk import System
#from mavsdk.geofence import Point, Polygon
from pymavlink import mavutil
import gphoto2cffi as gp
try:
    from dronekit import connect, VehicleMode, Command, LocationGlobal
    a = LocationGlobal(45.404395, -72.143708, 20)
    b = LocationGlobal(45.405081, -72.143752, 20)
    c = LocationGlobal(45.413699, -72.143969, 20)
    d = LocationGlobal(45.416463, -72.139731, 20)
    e = LocationGlobal(45.426051, -72.147345, 20)
    f = LocationGlobal(45.433061, -72.151400, 20)
    g = LocationGlobal(45.404395, -72.143708, 20)
    h = LocationGlobal(45.405081, -72.143752, 20)
    Adm_Home=LocationGlobal( 45.404464,-72.144521)
    Adm_1=LocationGlobal( 45.404315,-72.144480, 20)
    Adm_2=LocationGlobal( 45.404257,-72.144408, 20)
    Adm_3=LocationGlobal( 45.404278,-72.144296, 20)
    Adm_4=LocationGlobal( 45.404130,-72.144180, 20)
    Adm_5=LocationGlobal( 45.404485,-72.144404, 20)
    Adm_6=LocationGlobal( 45.404598, -72.144494, 20)
    Adm_7=LocationGlobal(  45.404621, -72.144688, 20)
    Adm_8=LocationGlobal( 45.405089, -72.145306, 20)
    Adm_9=LocationGlobal( 45.405255,-72.145806, 20)
    Adm_10=LocationGlobal(  45.405806, -72.146303, 20)
    Adm_11=LocationGlobal( 45.406321, -72.145937, 20)
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

dayLake = "Bromton_Day5_"
album = []
pic = ""
vehicle = None
drone_connected = False
lat = 0.0
lon = 0.0
fix = 0
hdop = 0
shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")
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
        nc = nclib.Netcat(('192.168.2.56', 9001))
        return nc
    except:
        print("could not connect to Emlid")


def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the process we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill that process!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
        if b'gvfs-gphoto2-volume-monitor' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
nc = connectEmlid()
killGphoto2Process()
my_cam = gp.Camera()
# shot_date = datetime.now().strftime("%Y-%m-%d") # This has been written to the while True loop.
# shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # This has been written to the while True loop.
picID = "_UbergaiterAcquisition_"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
timeCommand = ["--set-config datetime=$(date +%s)"]

folder_name = dayLake + picID
save_location = "/home/uberg/Documents/gphoto/images/" + folder_name
#save_location = "/media/uberg/photos/" + folder_name
def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)

# def captureImages():
#     # gp(triggerCommand)
#     imgdata = my_cam.capture()
#     shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")
#     print(shot_time)
#     sleep(3)
#     with open()
#     renameFiles(picID, shot_time)
#     shot_time = ""
#     num_pics_day = num_pics_day + 1
#     gp(clearCommand)

# def renameFiles(ID, shot_time_now):
#     for filename in os.listdir("."):
#         print(str(filename))
        
#         if len(filename) < 13:
#             if filename.endswith(".JPG"):
#                 os.rename(filename, (shot_time_now + ID + ".JPG"))
#                 print(str(filename))
#                 print("Renamed the JPG")
#             elif filename.endswith(".CR2"):
#                 os.rename(filename, (shot_time_now + ID + ".CR2"))
#                 print("Renamed the CR2")


# class Target:
#   def __init__(self, name, latitude, longitude):
#     self.name = name
#     self.latitude = latitude
#     self.longitude = longitude



    
async def armDrone():
    if drone_connected == True:
        try: 
                vehicle.armed = True
                if vehicle.armed == True:
                        vehicle.mode = VehicleMode("GUIDED") ## guided is recommended for on the fly 
                        if vehicle.mode.name == "GUIDED":
                                print ("drone is armed and ready in GUIDED mode")
                                # goTo_DK(coordA2_P)
                                return vehicle
                        else: print("drone can't get in GUIDED mode")
                else: print("drone can't arm")
        except:
                print("can't arm drone")
   
    
async def cross_Distance(target, vehicle):
    #await asyncio.sleep(3)
    print (f"going to : latitude : {target.lat}  longitude: {target.lon}")
    dist = 1000.0
    lat = target.lat
    lon = target.lon
    targetLoc = LocationGlobal(lat,lon,20)
    drone = vehicle
    drone.simple_goto(targetLoc)

    #await drone.action.set_current_speed(10)
    #await drone.action.goto_location(lat,lon, 230, 0)

    while dist > 0.2:
        locA = (lat, lon) #46.404395, -72.143708
        locBlat = 0.0
        locBlon = 0.0
        currentLocation = vehicle.location.global_relative_frame
        locBlat = currentLocation.lat
        locBlon = currentLocation.lon
        gpsInfo = vehicle.gps_0
        fix = gpsInfo.fix_type
        hdop = gpsInfo.eph
        # async for position in drone.telemetry.position():
        #     locBlat = position.latitude_deg
        #     locBlon = position.longitude_deg
        #     print(locBlat, locBlon)
        #     break
        dist = hs.haversine(locA,(locBlat, locBlon),unit=Unit.METERS)
        print(f"dist = {dist}")
        #######
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
        #######
        await take_screen(lat,lon,fix,hdop, x,y,z,ns,cmPrecision, time)
    print(f"arrived at {target.name}")

async def connectDrone():
    # try:
    #     try:
    print("trying to connect ....")
    vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=115200) ### raspberry pi
    print("connected to drone through raspberry pi")
    print ("Vehicle status:", vehicle.system_status.state)
    drone_connected = True
    if drone_connected == True:
        try: 
                vehicle.armed = True
                if vehicle.armed == True:
                        vehicle.mode = VehicleMode("GUIDED") ## guided is recommended for on the fly 
                        if vehicle.mode.name == "GUIDED":
                                print ("drone is armed and ready in GUIDED mode")
                                # goTo_DK(coordA2_P)
                                return vehicle
                        else: 
                            print("drone can't get in GUIDED mode")
                            return vehicle
                else: print("drone can't arm")
        except:
                print("can't arm drone")
    


# async def take_picture(drone):
    
#     #async for position in drone.telemetry.raw_gps():
#         #print(position)
#         # print(position.timestamp_us)
#         #print(position.latitude_deg)
#         # print(position.longitude_deg)
#         #print(position.horizontal_uncertainty_m)
#         #print(position.hdop)
        
#         pic = str(position.timestamp_us) + "-" + str(position.latitude_deg) + "-" +str(position.longitude_deg) + "-" +str(position.hdop) #+ ".jpg"
        
#         return pic    
        
#         #print(pic)
#         #album.append(pic)
#         #print(album)


# async def print_battery(drone):
#     async for battery in drone.telemetry.battery():
#         print(f"Battery: {battery.remaining_percent}")


# async def print_gps_info(drone):
#     async for gps_info in drone.telemetry.gps_info():
#         print(f"GPS info: {gps_info}")


# async def print_in_air(drone):
#     async for in_air in drone.telemetry.in_air():
#         print(f"In air: {in_air}")

# async def get_position(drone):
#     position = drone.telemetry.position()
#     return position
# async def print_position(drone):
#     async for position in drone.telemetry.position():
#         print(position)


async def take_screen(lat,lon,fix,hdop, x,y,z,ns,cmPrecision, time):
    global save_location
    global countPics
    global dayLake
#    global vehicle
    #killGphoto2Process()
#    position = vehicle.location.global_frame
#    gps = vehicle.gps_0
#    print(position)
    # img = ImageGrab.grab(bbox=(0, 1000, 100, 1100)) #x, y, w, h
    # img_np = np.array(img)
#    pic = str(position.lat) + "-" +str(position.lon) + "-" #+ ".jpg"
#    hdop =  str(gps.fix) + "-" + str(gps.num_sat) + "-"
    #picName = str(lat) + "_" + str(lon) + "_" + str(fix) + "_" + str(hdop) + "_" + str(x) + "_" + str(y) + "_" + str(z) + "_" + str(ns) + "_" + str(cmPrecision) + "_" + str(time)
    picName = "_" + str(lat) + "_" + str(lon) + "_" + str(fix) + "_" + str(hdop)
    #picName = await take_picture(drone)
    #shot_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
    
    picTag = dayLake + shot_time + "picNo_" + str(countPics) + picName + ".png"
    completeName = os.path.join(save_location, picTag)
    imgdata = my_cam.capture() 
    with open(completeName, "wb") as binary_file:
        binary_file.write(imgdata)

       # shot_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S_")
    sleep(1)
    countPics = countPics + 1
    #gp(downloadCommand)
    
    # renameFiles(picID, shot_time)
    # for filename in os.listdir("."):
    #     print(str(filename))
        
    #     if len(filename) < 13:
    #         if filename.endswith(".JPG"):
    #             os.rename(filename, (shot_time + picID + ".JPG"))
    #             print(str(filename))
    #             print("Renamed the JPG")
    #         elif filename.endswith(".CR2"):
    #             os.rename(filename, (shot_time + picID + ".CR2"))
    #             print("Renamed the CR2")

    #num_pics_day = num_pics_day + 1

    #shot_time = ""
    #gp(clearCommand)
    # captureImages()
    # cv2.imwrite(picName, img_np)
    print(f"took {picTag} in picture")
    #await asyncio.sleep(3)
        
# async def print_raw_position(drone):
#     async for position in drone.telemetry.raw_gps():
#         print(position.timestamp_us)
#         return position
###########
# async def main():
#     """
#     Launching a specific pygame window retrieves and works according to the received commands.
#     :return:
#     """

#     running = True

#     while running:

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         keys = pygame.key.get_pressed()

#         # While being in air and landing mode the drone is not likely to takeoff again, so
#         # a condition check is required here to avoid such a condition.

#         if keys[pygame.K_UP] and (await print_in_air(drone) != True):
#             print("going b")
#             await drone.action.goto_location(45.405081, -72.143752, flying_alt, 0)

#         elif keys[pygame.K_DOWN]:
#             print("going g")
#             await drone.action.goto_location(45.404395, -72.143708, flying_alt, 0)

#         elif keys[pygame.K_RIGHT]:
#             await print_position(drone)

#         elif keys[pygame.K_i]:
#             await info(drone)
 ############
 ############
async def run():
    # Init the drone
    #drone = System()
    #await drone.connect(system_address="serial:///dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00-1-GROUND ROVER")
    #print("trying to connect ....")
    vehicle = await connectDrone()

    print("connected, continuing process")
    
    #await drone.connect(system_address="serial:///dev/serial/by-id/usb-Hex_ProfiCNC_CubeBlack_47003C000651383438333530-if00:115200")
    # Start the tasks
    #asyncio.ensure_future(print_battery(drone))
    #asyncio.ensure_future(print_gps_info(drone))
    #asyncio.ensure_future(print_in_air(drone))
    #asyncio.ensure_future(print_position(drone))
    #asyncio.ensure_future(get_position(drone))
    #asyncio.ensure_future(print_raw_position(drone))
    #asyncio.ensure_future(take_picture(drone))
    #asyncio.ensure_future(cross_Distance(drone, a))

    # targets
    ################
    killGphoto2Process()
    #gp(clearCommand)
    createSaveFolder()

    a = LocationGlobal(45.404395, -72.143708, 20)
    b = LocationGlobal(45.405081, -72.143752, 20)
    c = LocationGlobal(45.413699, -72.143969, 20)
    d = LocationGlobal(45.416463, -72.139731, 20)
    e = LocationGlobal(45.426051, -72.147345, 20)
    f = LocationGlobal(45.433061, -72.151400, 20)
    g = LocationGlobal(45.404395, -72.143708, 20)
    h = LocationGlobal(45.405081, -72.143752, 20)

    

    # print("Waiting for drone to connect...")
    # async for state in drone.core.connection_state():
    #     if state.is_connected:
    #         print(f"-- Connected to drone!")
    #         break

    #print("Waiting for drone to have a global position estimate...")
    # async for health in drone.telemetry.health():
    #     print(f"Health{health}")
    #     if health.is_global_position_ok and health.is_home_position_ok:
    #         print("-- Global position state is good enough for flying.")
    #         break

    # print("Fetching amsl altitude at home location....")
    # async for terrain_info in drone.telemetry.home():
    #     absolute_altitude = terrain_info.absolute_altitude_m
    #     break
    await asyncio.sleep(5) 
    
       
    #print("-- Arming")
    #await armDrone()
   # await drone.action.arm()

   # print("-- Taking off")
   # await drone.action.takeoff()
    
    


    #####
    #print("Fetching home location coordinates...")
    #async for terrain_info in drone.telemetry.home():
    #    latitude = terrain_info.latitude_deg
    #    longitude = terrain_info.longitude_deg
    #	break

    # await asyncio.sleep(1)

    # # Define your geofence boundary
    # p1 = Point(latitude - 0.0001, longitude - 0.0001)
    # p2 = Point(latitude + 0.0001, longitude - 0.0001)
    # p3 = Point(latitude + 0.0001, longitude + 0.0001)
    # p4 = Point(latitude - 0.0001, longitude + 0.0001)

    # # Create a polygon object using your points
    # polygon = Polygon([p1, p2, p3, p4], Polygon.FenceType.INCLUSION)

    # # Upload the geofence to your vehicle
    # print("Uploading geofence...")
    # await drone.geofence.upload_geofence([polygon])

    # print("Geofence uploaded!")
    ####
    # To fly drone 20m above the ground plane
    #flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    # print("going a")
    # dist = 1000.0
    # await drone.action.goto_location(45.404395, -72.143708, flying_alt, 0)
    # await take_screen(drone)
    # while dist > 0.2:
    #     locA = (45.404395, -72.143708)
    #     locBlat = 0.0
    #     locBlon = 0.0
    #     async for position in drone.telemetry.position():
    #         locBlat = position.latitude_deg
    #         locBlon = position.longitude_deg
    #         break
    #     dist = hs.haversine(locA,(locBlat, locBlon),unit=Unit.METERS)
    #     print(dist)
    #     await take_screen(drone)
    
    timer = 0
# print("arrived at a")
    while(timer < 10000):
        currentLocation = vehicle.location.global_relative_frame
        lat = currentLocation.lat
        lon = currentLocation.lon
        gpsInfo = vehicle.gps_0
        fix = gpsInfo.fix_type
        hdop = gpsInfo.eph

        await take_screen(lat,lon,fix,hdop,x,y,z,ns,cmPrecision,time)
        timer = timer+1    
  #  await cross_Distance(Adm_1, vehicle)
   # await cross_Distance(Adm_2, vehicle)
    #await cross_Distance(Adm_3, vehicle)
    #await cross_Distance(Adm_4, vehicle)
    #await cross_Distance(Adm_5, vehicle)
    #await cross_Distance(Adm_Home, vehicle)
    ##await cross_Distance(f, vehicle)
    
    #await cross_Distance(h, vehicle)
   # vehicle.close()
    print(f"mission over with {num_pics_day} pictures taken")
    

 ########   
 ########    
if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())
    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
