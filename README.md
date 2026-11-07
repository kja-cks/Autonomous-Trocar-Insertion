# Autonomous-Trocar-Insertion
Project I did from 11 -> to 12th grade. All code in this repository was used for troubleshooting and testing a robotic arm end-effector that could position itself around patients and safely insert trocars.

OpenCV library was used for ArUco marker identification and orientation, and stereo sensing was used to determine position relative to camera, Once Identified robot travels to the marker through a stepper motor. As robot performs insertion axial forces are measured and through measuring how forces change over time layers of tissue are identified and are able to stop insertion. Marker coordinates were also sent to the Universal Robotics simulator via the internet using the UR_RTDE library to model robot end effector positioning
