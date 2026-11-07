import rtde_control
import rtde_receive

ROBOT_IP = "192.168.0.197"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

target_pose = [0,0,0,0,0,0]

rtde_c.moveL(target_pose, speed=0.3, acceleration=0.5)

rtde_c.disconnect()
print("complete")