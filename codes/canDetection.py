import cv2
import numpy as np
import statistics

def center_location(cn):
    cap = cv2.VideoCapture(cn)
##    cap.set(3, 1280)
##    cap.set(4, 720)

    if cn == 2:
        lower_red = np.array([160, 140, 120])
        upper_red = np.array([179, 255, 255])
        
    if cn == 1:
        lower_red = np.array([110, 137, 70])
        upper_red = np.array([179, 255, 255])

    if cn == 0:
        lower_red = np.array([0, 80, 145])
        upper_red = np.array([8, 255, 255])
        
    center_x = []
    center_y = []


    while True:
        ret, image = cap.read()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        frame = image
        blur = cv2.GaussianBlur(hsv, (7, 7), 0)
        thresh_red = cv2.inRange(hsv,lower_red, upper_red)
        res = cv2.cvtColor(thresh_red, cv2.COLOR_GRAY2BGR)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(res, kernel, iterations=4)
        
        red_final = cv2.Canny(dilate, 75, 200)
        cv2.imshow('canny', dilate)
        contours_red, _ = cv2.findContours(red_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour = max(contours_red, key = cv2.contourArea)

##        for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        center_x.append(x+w)
        center_y.append(y+h)
    
##        if len(center_x) > 50:
##            x1 = int(statistics.mean(center_x))
##            y1 = int(statistics.mean(center_y))
##            break

        if cv2.waitKey(30) & 0xff == 27:
            break
        
        cv2.imshow('frame', image)
    
    cap.release()
    cv2.destroyAllWindows()
##    return x1, y1, frame

center_location(2 )
