import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import time

#Game Menu
menu=1
game_choice=0

#Game vars
cx,cy,cx_bait,cy_bait = 250,250,500,500
color = (64,133,210)
counter = 0
wrong_counter = 0
score=0
total_time=10
start_time = time.time()
number= random.randint(1,5)
wrong_number = random.randint(1,5)
wrong_time = random.randint(0,1)



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



#reaction time game
while True :
    success,img = cap.read()
    #Games Menu

    if menu == 1:
        cvzone.putTextRect(img, f"Measure Your Abilities With Brain Games", (200, 70), colorR=(139, 61, 72), scale=2)
        cvzone.putTextRect(img,f'Games: ',(40,200),colorR=(139, 61, 72),scale=3)
        cvzone.putTextRect(img,f'1-Reaction Time',(40,270),colorR=(32,165,218),scale = 2)
        cvzone.putTextRect(img, f'2-Amine\'s 2nd game' , (40, 340), colorR=(32, 165, 218), scale=2)
        cvzone.putTextRect(img, f'\'q\' to Quit ', (40, 410), colorR=(0, 0, 128), scale=2)
        game_choice = cv2.waitKey(1)
        if game_choice in [49,50,51]:
            menu = 0
        elif game_choice == 113:
            cv2.destroyAllWindows()
            break

    match game_choice:
        #game 1 : reaction_time
        case 49:
            timer = int(total_time - int(time.time() - start_time))
            if timer >= 0:
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
                            elif fingers.count(1) == wrong_number:
                                wrong_counter = 1
                        case 2:

                            if fingers.count(1) == 2:
                                color = (0, 255, 0)
                                counter = 1
                            elif fingers.count(1) == wrong_number:
                                wrong_counter = 1

                        case 3:

                            if fingers.count(1) == 3:
                                color = (0, 255, 0)
                                counter = 1
                            elif fingers.count(1) == wrong_number:
                                wrong_counter = 1

                        case 4:
                            if fingers.count(1) == 4:
                                color = (0, 255, 0)
                                counter = 1
                            elif fingers.count(1) == wrong_number:
                                wrong_counter = 1

                        case 5:

                            if fingers.count(1) == 5:
                                color = (0, 255, 0)
                                counter = 1
                            elif fingers.count(1) == wrong_number:
                                wrong_counter = 1

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
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 600)

                            wrong_number=random.randint(1,5)
                            while (number == wrong_number):
                                wrong_number=random.randint(1,5)
                            wrong_time = random.randint(0,1)
                            if wrong_time == 1:
                                cx_bait = random.randint(100, 1100)
                                cy_bait = random.randint(100, 600)
                            else:
                                wrong_number = -2
                    if wrong_counter:
                        wrong_counter += 1
                        if wrong_counter == 3:
                            score -=10
                            number = random.randint(1, 5)
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 600)

                            wrong_number = random.randint(1, 5)
                            while (number == wrong_number):
                                wrong_number = random.randint(1, 5)
                            wrong_time = random.randint(0, 1)
                            if wrong_time == 1:
                                cx_bait = random.randint(100, 1100)
                                cy_bait = random.randint(100, 600)
                            else:
                                wrong_number = -2

                #Button
                cv2.putText(img,f"{number}",(cx-50,cy),cv2.FONT_HERSHEY_SIMPLEX,1,(15,37,144),2,cv2.LINE_AA)
                cv2.circle(img,(cx,cy),30,color,cv2.FILLED)
                cv2.circle(img, (cx, cy), 10,(255,255,255), cv2.FILLED)
                cv2.circle(img, (cx, cy), 20, (255, 255, 255),2)
                cv2.circle(img, (cx, cy), 30, (0,0,0), 2)
                cv2.imshow("Image",img)
                cv2.waitKey(1)

                #Bait Button
                if wrong_time == 1:
                    cv2.circle(img, (cx_bait, cy_bait), 30, (0,0,255), cv2.FILLED)
                    cv2.putText(img, f"{wrong_number}", (cx_bait - 50, cy_bait), cv2.FONT_HERSHEY_SIMPLEX, 1, (15, 37, 144), 2, cv2.LINE_AA)
                    cv2.circle(img, (cx_bait, cy_bait), 10, (255, 255, 255), cv2.FILLED)
                    cv2.circle(img, (cx_bait, cy_bait), 30, (0, 0, 0), 2)
                    cv2.circle(img, (cx_bait, cy_bait), 20, (255, 255, 255), 2)


                #HUD
                cvzone.putTextRect(img ,f'Timer : {timer}',(1000,75),scale=2,colorR=(0,0,255))
                cvzone.putTextRect(img, f'Score:{score}', (100, 75), scale=2,colorR=(0,0,255))
            else:
                cv2.putText(img,f'Score :{score}',(500,300),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,200),5)
                cvzone.putTextRect(img, ' press "P" to Play  / Q to Go back to Menu ', (400, 400), scale=2, colorR=(0, 0, 255))
        #game 2 :
        #case 50:




    cv2.imshow("Image",img)
    key =cv2.waitKey(1)
    #Restart the Game
    if key == ord('p'):
        counter = 0
        wrong_counter = 0
        score = 0
        total_time = 10
        timer=10
        start_time = time.time()
    #Quit the Game
    elif key == ord('q'):
        menu = 1

