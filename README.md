# smart-robot-hand
### Smart Robotic Arm
This repository hosts the comprehensive thesis project titled "Smart Robotic Arm" (alternatively referred to as "Smart Robotic Hand" throughout the document), a capstone endeavor for the Bachelor of Technology in Mechatronics Engineering. Authored by Miheer Diwan (Roll No. H016) and Shubhankar Kulkarni (Roll No. H024) at SVKM’s NMIMS Mukesh Patel School of Technology Management & Engineering (MPSTME), Mumbai, India, this work was completed during the 2021-22 academic year.

The project addresses critical challenges in human-robot interaction for hazardous environments, such as radioactive facilities or industrial settings prone to accidents. It introduces a multipurpose, dexterous robotic arm/hand designed to minimize risks to human life and property by enabling remote or automated manipulation of objects. The system operates in two primary modes:

- Autonomous Mode: Utilizes advanced computer vision techniques, including 3D object detection via camera triangulation (e.g., Direct Linear Transformation or DLT calculations and stereo calibration), to precisely locate objects in three-dimensional space. Once detected, the arm calculates trajectories, picks up the object, and dynamically adjusts grip strength based on the object's weight, material, and fragility—ensuring safe handling without damage. This mode supports repeatable tasks, such as placing objects at user-designated locations or performing operations multiple times as specified.
- Gesture Control Mode: Allows real-time remote control through hand gestures captured by cameras, without requiring the user to wear any equipment. Leveraging pose estimation (e.g., arm-pose and hand-pose detection), the system replicates human motions with high accuracy and low latency, enabling intuitive operation from a safe distance. This is particularly useful in scenarios where human precision is needed but direct involvement is dangerous, such as manufacturing delicate chipsets or medical procedures.

The full 47-page report PDF [Report](report.pdf) is included in this repository, complete with detailed chapters on methodology, mechatronic system analysis (mechanical design, programming, trajectory, and drive systems), testing results (e.g., object reaching and lifting demonstrations), advantages/limitations, and future scope (e.g., enhancing DOF or integrating AI). Appendices provide soft code flowcharts and a component list for replication. For inquiries, contact the authors via NMIMS or professional networks.

## Tools Used:
1. Python
2. CoppeliaSim
3. OpenCV
4. MATLAB/Simulink
5. Solidworks
6. Arduino
7. MediaPipe
8. Direct Linear Transform (DLT)

## Model Demonstration
https://github.com/user-attachments/assets/415d8024-d692-4531-bcd2-876b541c1dd8
