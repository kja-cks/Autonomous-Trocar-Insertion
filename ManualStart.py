import rtde_control
import rtde_receive
import numpy as np
import cv2
import time
from scipy.spatial.transform import Rotation as R

print("imported")
ROBOT_IP = '192.168.0.197'

##CONNECTING TO ROBOT
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

rtde_c.setTcp([0,.05,.337,0,0,0])

camX = (1 - np.random.rand() + np.random.rand())
camY = (1 - np.random.rand() + np.random.rand())
camZ = np.random.rand()

arRotX = 0
arRotY = .11
arRotZ = .125

print(camX, camY, camZ)
camTransVec = np.array([0.100, -.25, 0.11])
camRotVec = np.array([0, -(np.pi)*.9, 0])

arucoTransVec = np.array([.018, 0.008, 0.011])
arucoRotVec = np.array([arRotX, arRotY, arRotZ])

def ArUcoPoistioning(markerTrans, markerRot, camTrans, camRot):

    transVec = markerTrans
    print ("Stereo Sensor Output:", transVec)
    for i in range(3):
        if i == 0:
            axis = np.array([1, 0, 0])  #Rotating around X axis
        elif i == 1:
            axis = np.array([0, 1, 0])  #Rotating around Y axis
        elif i == 2:
            axis = np.array([0, 0, 1])  #Rotating around Z axis

        angle = camRot[i]
        rot_vec = axis * angle
        rotation = R.from_rotvec(rot_vec)
        transVec = rotation.apply(transVec)
        print(transVec)
        milk = transVec + camTrans
        cookies = markerRot + camRot

    return milk, cookies, camTrans

arucoPos, arucoRot, movedCam = ArUcoPoistioning(arucoTransVec, arucoRotVec, camTransVec, camRotVec)

print("ArUco Pose in Reference to Robot", arucoPos)
print("ArUco Rotation in Reference to Robot", arucoRot)
print("Camera Pose in Reference to Robot", movedCam)

current = rtde_r.getActualTCPPose()
#print("Starting TCP Pose:", current)

targetPose = np.append(arucoPos, arucoRot)
print(targetPose)
q_solutions = rtde_c.getInverseKinematics(targetPose)

rtde_c.moveL(targetPose, speed=0.05, acceleration=0.03)
current = rtde_r.getActualTCPPose()
print("Moved Position:", current)

target = np.array(targetPose[:3])
actual = np.array(rtde_r.getActualTCPPose()[:3])

positionError = np.linalg.norm(target - actual)
print("Position Error:", positionError)

xangle_error = np.arccos(np.clip(np.dot(targetPose[3], current[3]),  -1, 1))
print("X Angle Error:", xangle_error)

yangle_error = np.arccos(np.clip(np.dot(targetPose[4], current[4]),  -1, 1))
print("Y Angle Error:", yangle_error)

zangle_error = np.arccos(np.clip(np.dot(targetPose[5], current[5]),  -1, 1))
print("Z Angle Error:", zangle_error)

q_sol = rtde_c.getInverseKinematics(targetPose)
q_seed = rtde_r.getActualQ()

print(q_sol)
print(q_seed)

def joint_distance(q1,q2):
    return np.linalg.norm(np.array(q1) - np.array(q2))

#print(joint_distance(q_seed, q_sol))