from pymavlink import mavutil 
print("hi im droneControl")
import time
import math
vehicle = None
drone_connected = False
coordA1_P = None
coordA2_P = None
coordB1_P = None
coordB2_P = None
coordC1_P = None       
coordC2_P = None
coordC3_P = None
coordHome_P = None 
try:
    from dronekit import connect, VehicleMode, Command, LocationGlobal
    coordA1_P = LocationGlobal( 45.513762, -73.531807, 20)
    coordA2_P = LocationGlobal( 45.513733, -73.531755,20)
    coordB1_P = LocationGlobal( 45.513679, -73.531842,20)
    coordB2_P = LocationGlobal( 45.513673, -73.531771,20)
    coordC1_P = LocationGlobal( 45.513582, -73.531883,20)
    coordC2_P = LocationGlobal(45.513638, -73.531816,20)
    coordC3_P = LocationGlobal( 45.513584, -73.531783,20)
    coordHome_P = LocationGlobal( 45.513582, -73.531883,20) 
    print("imported dronekit")
except ImportError:
    print("can't import dronekit")

def connectDrone():   
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

def get_distance_metres(aLocation1, aLocation2):
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def goto(targetLocation):
        currentLocation = vehicle.location.global_relative_frame      
        print(type(currentLocation))
        gpsInfo = vehicle.gps_0
        print(gpsInfo.fix_type)
        print(coordA1_P.lat)
        targetDistance = get_distance_metres(currentLocation, targetLocation)
        vehicle.simple_goto(targetLocation)
        while vehicle.mode.name=="GUIDED":               
                remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
                if remainingDistance<=targetDistance*0.03: 
                        return("Reached target")
                        break
                        time.sleep(2)
        if (vehicle.mode.name=="HOLD"):
                return("fence hit")

def goTo_DK(coords):      
        vehicle.simple_goto(coords)
        print("going to a1") 
        goto(coords)
        print("going to a1 ")
   
vehicle = connectDrone()
goTo_DK(coordA1_P)
vehicle.close()
