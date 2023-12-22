import cv2
import numpy as np
import json
#from datetime import datetime, timedelta
vRadius = 50
def drawCircles(frame , circles):     
    side_movement = "Stable"
    forward_movement = "Stable"
    speed = "slow"
    result_dict = {"forward_movement": forward_movement,
                   "side_movement": side_movement,
                   "speed": speed
                   }
    for i in circles[0, :]:
        x, y, r = i[0], i[1], i[2]
        cv2.circle(frame, (x, y), r, (255, 255, 0), 3)
        threshold =7
        lThreshold=5
        mThreshold=10
        #hthreshold=7


        if abs(x - center_x)<threshold:
            side_movement = "Stable"
        elif(center_x-x)>threshold:
            side_movement = "Left"
        elif(x-center_x)>threshold:
            side_movement = "Right"

        if abs(vRadius-r)<threshold:
            forward_movement = "Stable"
        elif(vRadius-r)>threshold:
            forward_movement="Forward"
        elif(r-vRadius)>threshold:
            forward_movement = "Backward"

        if(abs(vRadius-r)<lThreshold):
            speed="stop"
        elif (abs(vRadius-r)>lThreshold) and (abs(vRadius-r)<mThreshold):
            speed="low"
        elif (abs(vRadius-r)>mThreshold):
            speed="high"

        result_dict = {
            "forward_movement":forward_movement,
            "side_movement": side_movement,
            "speed": speed
        }
        print(json.dumps(result_dict, indent=4))

def detectCircles(frame):
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    circles = cv2.HoughCircles( blur ,
                                cv2.HOUGH_GRADIENT,
                                dp =.65 ,

                                minDist= 20,
                                param1 = 68,
                                param2 = 52,
                                minRadius = 25,
                                maxRadius = 100,)


    if circles is not None:
        circles = np.uint16(np.around(circles))
        drawCircles(frame, circles)



import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 250)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

center_x = width // 2
center_y = height // 2

#print("Center Coordinates: ({}, {})".format(center_x, center_y))
'''print(center_x)
print(center_y)
print(width)
print(height)'''
while True:
    ret , frame = cap.read()
    frame = cv2.flip(frame , 1)


    detectCircles(frame)

    cv2.circle(frame, (center_x, center_y), vRadius-5, (0, 255, 0), 2)
    cv2.circle(frame, (center_x, center_y), vRadius+7, (0, 255, 0), 2)
    cv2.line(frame, (center_x,0), (center_x,frame.shape[0]), (255, 0, 0), 2)
    cv2.line(frame, (0,center_y), (frame.shape[1],center_y), (255, 0, 0), 2)
    #print(frame.shape)
    cv2.imshow("Frame ", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break