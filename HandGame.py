import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import time


#Game vars
cx,cy = 250,250
color = (64,133,210)
counter = 0
score=0
timer=0
total_time=10
start_time=time.time()
number= random.randint(1,5)
#cam
cap=cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
#Find the Polynomial equation (2nd degree)

x=[300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y= [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] #values in cm

#y=Ax^2 +Bx + C

coff = np.polyfit(x,y,2)
#Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=2)

while True :
    success,img = cap.read()

    if timer <= 10:
        hands, img = detector.findHands(img, draw=False)
        if hands:
            fingers = detector.fingersUp(hands[0])
            lmlist = hands[0]['lmList']
            x,y,w,h =hands[0]['bbox']
            x1,y1,z1 = lmlist[5]
            x2,y2,z2 = lmlist[17]

            #measuring approximate distance
            distance = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            A, B, C = coff
            distanceCm = A * distance ** 2 + B * distance + C

            match number:
                case 1:

                    if fingers.count(1)== 1:
                        color = (0, 255, 0)
                        counter = 1

                case 2:

                    if fingers.count(1) == 2:
                        color = (0, 255, 0)
                        counter = 1

                case 3:

                    if fingers.count(1) == 3:
                        color = (0, 255, 0)
                        counter = 1

                case 4:
                    if fingers.count(1) == 4:
                        color = (0, 255, 0)
                        counter = 1

                case 5:

                    if fingers.count(1) == 5:
                        color = (0, 255, 0)
                        counter = 1

                case _:
                    color = (64,133,210)

            cvzone.putTextRect(img,f"{int(fingers.count(1))}Up",(x,y),colorR=(0,255,0))
            cv2.rectangle(img,(x,y),(x+w , y + h),(0,255,0),3)
        # counter
            if counter:
                counter +=1
                if counter == 3:
                    score+=10
                    color = (64, 133, 210)
                    number= random.randint(1,5)
                    cx = random.randint(100,1100)
                    cy = random.randint(100,600)

        #Button
        cv2.putText(img,f"{number}",(cx-50,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(15,37,144),2,cv2.LINE_AA)
        cv2.circle(img,(cx,cy),30,color,cv2.FILLED)
        cv2.circle(img, (cx, cy), 10,(255,255,255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255),2)
        cv2.circle(img, (cx, cy), 30, (0,0,0), 2)
        cv2.imshow("Image",img)
        cv2.waitKey(1)

        #HUD
        timer= abs(int(total_time - (time.time() - start_time)))
        cvzone.putTextRect(img ,f'Timer : {timer}',(1000,75),scale=2,colorR=(0,0,255))
        cvzone.putTextRect(img, f'Score:{score}', (100, 75), scale=2,colorR=(0,0,255))
    else:
        cv2.putText(img,f'Score :{score}',(500,300),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,200),5)
        cv2.putText(img,f"Game Over",(400,400),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,200),10)
        cvzone.putTextRect(img, ' press "R" to Play Again / Q to Quit ', (600, 500), scale=2,colorR=(0,0,255))


    cv2.imshow("Image",img)
    key =cv2.waitKey(1)
    #Restart the Game
    if key == ord('r'):
        counter = 0
        score = 0
        total_time = 0
        timer=0
        start_time = time.time()
        current_time=0
    #Quit the Game
    elif key == ord('q'):
        cv2.destroyAllWindows()
        break

