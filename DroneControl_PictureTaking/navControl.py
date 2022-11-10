from pymavlink import mavutil
from dronekit import connect, VehicleMode, Command, LocationGlobal

try:
    vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=115200) ### raspberry pi
    vehicle.mode = VehicleMode("HOLD")
    print ("Vehicle status:", vehicle.system_status.state)
    print ("connected to drone through raspberry pi from script")
    vehicle.parameters['SERVO1_FUNCTION']=26.0 #'groundsteering'
    vehicle.parameters['SERVO3_FUNCTION']=70.0 #'throttle'
    print(vehicle.parameters['SERVO1_FUNCTION'])
    print(vehicle.parameters['SERVO3_FUNCTION'])
    print("Vehicle controlled by nav")
except:
    vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=115200) ### raspberry pi
    vehicle.mode = VehicleMode("HOLD")
    print ("Vehicle status:", vehicle.system_status.state)
    print ("connected to drone through raspberry pi from script")
    vehicle.parameters['SERVO1_FUNCTION']=26.0 #'groundsteering'
    vehicle.parameters['SERVO3_FUNCTION']=70.0 #'throttle'
    print(vehicle.parameters['SERVO1_FUNCTION'])
    print(vehicle.parameters['SERVO3_FUNCTION'])
    print("Vehicle controlled by nav")
    vehicle.close()
