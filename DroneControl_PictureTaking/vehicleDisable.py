from pymavlink import mavutil
from dronekit import connect, VehicleMode, Command, LocationGlobal

try:
    vehicle = connect('/dev/ttyACM0', wait_ready=False, baud=115200) ### raspberry pi
    vehicle.mode = VehicleMode("HOLD")
    print ("Vehicle status:", vehicle.system_status.state)
    print ("connected to drone through raspberry pi from script")
    vehicle.close()
    print("Vehicle closed")
except:
    vehicle = connect('/dev/ttyACM0', wait_ready=False, baud=115200) ### raspberry pi
    vehicle.mode = VehicleMode("HOLD")
    print ("Vehicle status:", vehicle.system_status.state)
    print ("connected to drone through raspberry pi from script")
    vehicle.close()
    print("Vehicle closed")
