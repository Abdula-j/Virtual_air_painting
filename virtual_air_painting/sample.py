import cv2 as cv 
import mediapipe as mp
import time
import os
import numpy as np
def hell(lml,fgd): 
    fingers=[]
    if (lml[finger_tip_id[0]][1] < lml[finger_tip_id[0] - 1][1]): 
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):

        if (lml[finger_tip_id[i]][2] < lml[finger_tip_id[i] - 2][2]):
             fingers.append(1)
        else:

            fingers.append(0) 
    return fingers
print("hello")
brush_thickness = 15
eraser_thickness = 50
image_canvas =np.zeros((720,1280,3), np.uint8) 
xp,yp=0,0
finger_tip_id= [4,8,12,16,20] 
folderpath="Images/Images" 
mylist=os.listdir(folderpath) 
print(mylist)
overlay=[]
for inpath in mylist:
    image=cv.imread(f'{folderpath}/{inpath}')
    overlay.append(image)
print(len(overlay))
header=overlay[0] 
draw_color = (255,200,100)
pTime = 0
cTime = 0 
mphands=mp.solutions.hands
hands=mphands.Hands() 
cap=cv.VideoCapture(0) 
cap.set(3,1280)
cap.set(4,720)
cap.set(cv.CAP_PROP_FPS, 60)
while True:
    s,i=cap.read()
    i = cv.flip(i, 1)
    i[0:125,0:1280] = header
    imgRGB = cv.cvtColor(i, cv.COLOR_BGR2RGB) 
    mpDraw = mp.solutions.drawing_utils
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks: 
        lml=[]
        for handLms in results.multi_hand_landmarks:

#fingers=[]
            for id, lm in enumerate(handLms.landmark):

# print(id, lm)
                h, w, c = i.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

#print(id, cx, cy)
                lml.append([id, cx, cy])
#cv.circle(i, (cx, cy), 15, (225, 0, 225), cv.FILLED)
                mpDraw.draw_landmarks(i, handLms, mphands.HAND_CONNECTIONS)
        if(len(lml)!=0):
             #xp, yp = 0, 0 #print(lml)
#tip of index and middle finger
            x1,y1=lml[8][1:]
            x2, y2 = lml[12][1:]
#print([x1,x2,y1,y2]) 
            fingers=hell(lml,finger_tip_id) 
            print(fingers)
#print(fingers)
            if(fingers[1] and fingers[2]): 
                xp, yp = 0, 0
                if (y1 < 125):

                    if (360 < x1 < 520):


                        default_overlay = overlay[0] 
                        draw_color = (255, 0, 0)
                    elif (530 < x1 < 650):
                        default_overlay = overlay[1] 
                        draw_color = (47, 225, 245)
                    elif (680 < x1 < 790):
                        default_overlay = overlay[2] 
                        draw_color = (197, 47, 245)
                    elif (800 < x1 < 950):
                        default_overlay = overlay[3] 
                        draw_color = (53, 245, 47)
                    elif (1050 < x1 < 1280):
                        default_overlay = overlay[4] 
                        draw_color = (0, 0, 0)
                cv.rectangle(i, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv.FILLED)
                print("selection mode")
            if(fingers[1]and fingers[2]==False):
                if(xp==0 and yp==0):

                    xp,yp=x1,y1
                if (draw_color==(0,0,0)):

                    cv.line(i, (xp, yp), (x1, y1), draw_color, eraser_thickness) 
                    cv.line(image_canvas, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                else:

                    cv.line(i,(xp,yp),(x1,y1),draw_color,brush_thickness) 
                    cv.line(image_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
                cv.circle(i, (x1, y1), 15, draw_color, cv.FILLED)
                xp,yp=x1,y1 
                print("drawingmode")
        imgGray=cv.cvtColor(image_canvas,cv.COLOR_BGR2GRAY)
        _,imgInv=cv.threshold(imgGray,50,255,cv.THRESH_BINARY_INV) 
        imgInv=cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR) 
        i=cv.bitwise_and(i,imgInv)
        i=cv.bitwise_or(i,image_canvas) 
    cTime = time.time()
    fps = 1 / (cTime - pTime) 
    pTime = cTime
    cv.putText(i, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (225, 0, 225),3) 
    i=cv.addWeighted(i,1,image_canvas,0.5,0)
    cv.imshow("image",i) #cv.imshow("canvas",image_canvas) 
    cv.waitKey(20)




