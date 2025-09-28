# smart-robot-hand
### Smart Robotic Arm
This repository hosts the comprehensive thesis project titled "Smart Robotic Arm" (alternatively referred to as "Smart Robotic Hand" throughout the document), a capstone endeavor for the Bachelor of Technology in Mechatronics Engineering. Authored by Miheer Diwan (Roll No. H016) and Shubhankar Kulkarni (Roll No. H024) under the supervision of Prof. Dattatray Sawant and Prof. Amey Raut at SVKM’s NMIMS Mukesh Patel School of Technology Management & Engineering (MPSTME), Mumbai, India, this work was completed during the 2021-22 academic year.

The project addresses critical challenges in human-robot interaction for hazardous environments, such as radioactive facilities or industrial settings prone to accidents. It introduces a multipurpose, dexterous robotic arm/hand designed to minimize risks to human life and property by enabling remote or automated manipulation of objects. The system operates in two primary modes:

- Autonomous Mode: Utilizes advanced computer vision techniques, including 3D object detection via camera triangulation (e.g., Direct Linear Transformation or DLT calculations and stereo calibration), to precisely locate objects in three-dimensional space. Once detected, the arm calculates trajectories, picks up the object, and dynamically adjusts grip strength based on the object's weight, material, and fragility—ensuring safe handling without damage. This mode supports repeatable tasks, such as placing objects at user-designated locations or performing operations multiple times as specified.
- Gesture Control Mode: Allows real-time remote control through hand gestures captured by cameras, without requiring the user to wear any equipment. Leveraging pose estimation (e.g., arm-pose and hand-pose detection), the system replicates human motions with high accuracy and low latency, enabling intuitive operation from a safe distance. This is particularly useful in scenarios where human precision is needed but direct involvement is dangerous, such as manufacturing delicate chipsets or medical procedures.

Key technical contributions include degree-of-freedom (DOF) analysis, development of multiple CAD models for mechanical components (e.g., fingers, thumb, palm, forearm with servo motors, and base assembly), inverse kinematics calculations, PID-controlled trajectory generation for smooth motion, and programming for gesture recognition using libraries like OpenCV. The design draws from an extensive literature survey on humanoid robotics, referencing historical milestones (e.g., Da Vinci's 1495 arm, Unimate's 1961 industrial arm evolving to PUMA) and modern innovations (e.g., hybrid hands like the KU model for ambidexterity and LabView-based stepper motor control for medical accuracy).
The arm's hardware incorporates servo motors, Arduino PCBs for control, LM2596 buck converters for power management, and switched-mode power sources, with limitations noted such as reduced DOF constraining functionality, a smaller workspace due to scale, and material/motor dependencies limiting object types. Applications span hazardous zones (e.g., radiation-polluted areas), medical robotics (e.g., aiding laparoscopy via Hand-Assisted Laparoscopic Surgery or HALS-inspired designs), and industrial automation.

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

<video controls width="560" height="315">
  <source src="https://raw.githubusercontent.com/shubhankarKulk/smart-robot-hand/main/videos/hand_1_v2.mp4" type="video/mp4">
</video>