## Usage
In order to run the Inverse Kinematics Demonstration for the robot arm, please run the files in the following order:

1. Open the V-REP file ```ikDemo.ttt```
2. Launch the Python Script ```IKDemonstration.py```
3. Move the sphere in the file in the y and z plane to see the extent of the inverse kinematics manipulation

- ```ikinCalculation.py``` is the inverse kinematic calculation calculated mathematically to be relayed onto the 
robot arm.
- ```camAll.py``` is used for calculation of position of the object.
- ```canDetection.py``` is used for detecting an object, a red can in this case.
- ```armBodyPose.py``` is used for mimicking the human hand motion to the robot arm.
- folders camera_1_2 and camera_2_3 are used to store calibration data for both the cameras at the same time, so that accurate locations can be estimated for the object.
- the folder arduino has a collection of scripts helping to relay the angle data onto the actual robot.