import mediapipe as mp
import cv2
import numpy as np
import time
import serial
import math

class angleDetector():
    def __init__(self, mode = False, maxHands = 1, det_conf = 0.7, tra_conf = 0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.det_conf = det_conf
        self.tra_conf = tra_conf
        
        self.mpHands = mp.solutions.hands
        self.mpPose = mp.solutions.holistic
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.det_conf, self.tra_conf)
        self.pose = self.mpPose.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self, img, draw = True):
            
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res_hand = self.hands.process(imgRGB)

        if self.res_hand.multi_hand_landmarks:
            for handLms in self.res_hand.multi_hand_landmarks:
                if draw:            
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res_pose = self.pose.process(imgRGB)
        holistic = self.res_pose.pose_landmarks
        if holistic:
            if draw:
                self.mpDraw.draw_landmarks(img, holistic, self.mpPose.POSE_CONNECTIONS)
        return img

    def draw_finger_angles(self, img, joint_list, draw = True):

        angle_list = []
        if self.res_hand.multi_hand_landmarks:
            for hand in self.res_hand.multi_hand_landmarks:
                for joint in joint_list:
                    a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
                    b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
                    c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])

                    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                    angle = np.abs(radians*180.0/np.pi)

                    if angle > 180.0:
                        angle = 360 - angle
                    if draw:
                        cv2.putText(img, str(round(angle, 2)), tuple(np.multiply(b, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3, cv2.LINE_AA)
                    angle_list.append(int(angle))
                    
        return img, angle_list

    def draw_pose_angles(self, img, pose_list, draw = True):

        angle_list = []
        count = 0
        pose = self.res_pose.pose_landmarks
        
        if pose:
            for joint in pose_list:
                if count == 0 or count == 4 and self.res_hand.multi_hand_landmarks:
                    if self.res_hand.multi_hand_landmarks:
                        for hand in self.res_hand.multi_hand_landmarks:
                            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
                            b = np.array([pose.landmark[joint[1]].x, pose.landmark[joint[1]].y])
                            c = np.array([pose.landmark[joint[2]].x, pose.landmark[joint[2]].y])
                            break
                    else:
                        a = np.array([pose.landmark[joint[0]].x, pose.landmark[joint[0]].y])
                        b = np.array([pose.landmark[joint[1]].x, pose.landmark[joint[1]].y])
                        c = np.array([pose.landmark[joint[2]].x, pose.landmark[joint[2]].y])
                    
                else:
                    a = np.array([pose.landmark[joint[0]].x, pose.landmark[joint[0]].y])
                    b = np.array([pose.landmark[joint[1]].x, pose.landmark[joint[1]].y])
                    c = np.array([pose.landmark[joint[2]].x, pose.landmark[joint[2]].y])

                radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians*180.0/np.pi)
                        
                if angle > 180.0:
                    angle = 360 - angle

                if count == 2 or count == 3:
                    angle -= 90
                    if angle < 0:
                        angle = abs(angle) + 90
                        
                if draw:
                    cv2.putText(img, str(round(angle, 2)), tuple(np.multiply(b, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3, cv2.LINE_AA)
                angle_list.append(int(angle))
                count += 1

        count = 0
        return img, angle_list

def str_con(a):
    return ','.join(map(str, a))

def main(serial_start):
    
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = angleDetector()
    cap.set(3, 1280)
    cap.set(4, 720)

    if serial_start:
        ser = serial.Serial()
        usbport = 'COM7'
        ser = serial.Serial(usbport,9600, timeout=1)
        
    angle_list_prev = ['0', '0', '0', '0', '0']

    mem = []
    
    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        img = detector.findPose(img)
        
        joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17], [4, 3, 2]]
        pose_list = [[4, 16, 24], [16, 14, 12], [14, 12, 11], [12, 11, 13], [11, 13, 15], [13, 15, 4]]

        img, pose_list = detector.draw_pose_angles(img, pose_list)
        img, angle_list = detector.draw_finger_angles(img, joint_list)

        if not angle_list:
            angle_list = angle_list_prev
        else:
            angle_list = [str(abs(180 - int(x))) for x in angle_list]
        mem.append([angle_list])

        pose_angles = str_con(pose_list)
        hand_angles = str_con(mem[0][0])
        
        angles = hand_angles
        ser.write(angles.encode())
##        time.sleep(2)
        print(hand_angles)        
        if len(mem) == 2:
            mem.pop(0)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        k = cv2.waitKey(30) & 0xff
        if k == 27:
              break

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main(serial_start = True)
