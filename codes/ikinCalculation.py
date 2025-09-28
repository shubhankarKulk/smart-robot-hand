import numpy as np
import math
import time
import variables as robot
import serial

##goal = np.array([0.4, 0.2, 0.2])

def ikin(goal):
    lengths = robot()
    
    theta_1 = np.arctan(goal[1] / goal[0])
    theta_2 = 0
    theta_3 = 0
    theta_4 = 0
    
    if lengths.L1 > goal[-1]:
        A = math.sqrt(goal[0]**2 + (lengths.L1 - goal[-1])**2)
        phi3 = np.arccos((lengths.L2**2 + lengths.L3**2 - A**2) / (2*lengths.L2*lengths.L3))
        theta_3 = np.pi - phi3
        beta = np.arctan(goal[0] / (lengths.L1 - goal[-1]))

    if lengths.L1 < goal[-1]:
        A = math.sqrt(goal[0]**2 + (- lengths.L1 + goal[-1])**2)
        
        value = (lengths.L2**2 + lengths.L3**2 - A**2) / (2*lengths.L2*lengths.L3)

        phi3 = np.arccos(value)
        theta_3 = math.pi - phi3
        beta = np.arctan(goal[0] / ( - lengths.L1 + goal[-1]))

    alpha = np.arccos((lengths.L2**2 + A**2 - lengths.L3**2) / (2*lengths.L2*A))

    if theta_3 > 0:
        theta_2 = beta - alpha
    if theta_3 < 0:
        theta_2 = beta + alpha
    
    r1 = lengths.L2*np.cos(theta_2) + lengths.L3*np.cos(theta_3)
    
    if r1 > goal[0]:
        value = ( - goal[0] + r1) / lengths.L4

    if r1 < goal[0]:
        value = (goal[0] - r1) / lengths.L4
     
##        theta_4 = np.arccos(value)

    angles = np.array([np.degrees(theta_1), np.degrees(theta_2), np.degrees(theta_3), np.degrees(theta_4)])
    return angles

def arduino_operate(angles, serial_start):
    if serial_start:
        ser = serial.Serial()
        usbport = 'COM7'
        ser = serial.Serial(usbport,19200, timeout=.1)

        time.sleep(1)
        start = 's'
        ser.write(start.encode)
        time.sleep(1)
    
            
