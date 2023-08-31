# -*- coding: utf-8 -*-
"""
Created on Thu May 25 02:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Steven Bui
"""

import cv2
import numpy as np

cascade1 = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cascade2 = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cascade3 = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture('Testt.webm')
hor= np.hstack((cap,cap))
#cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
dotlist= []



def close(frame,dot):
    # iterate over the frame compares to every dot to every other dot
        for ddot2 in frame:
            x, y = ddot2
            x0, y0 = dot
            if abs(x-x0)< 50 and abs(y-y0) <50 and ddot2 != dot:
                return True

        return False



while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    count =0
    frameone= []
    for contour in contours:


        if cv2.contourArea(contour) < 700:  # not much movement
            continue
        count += 1
        (x, y, w, h) = cv2.boundingRect(contour)
        crop_img = frame1[y:y + h, x:x + w]


        body1 = cascade1.detectMultiScale(crop_img)
        body2 = cascade2.detectMultiScale(crop_img)
        body3 = cascade3.detectMultiScale(crop_img)


        a=cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        center=(x+ int(w/2),y + int(h/2))



        frameone.append(center)

    dotlist.append(frameone)
    if len(dotlist)>10:
        dotlist.pop(0)

    for index,frame in enumerate(dotlist):

        for dot in frame:
            if close(frame,dot):
                col = (0,0,255)
                current = cv2.circle(frame1, dot, 2, col, 2)
            else:
                col= (0,255,255-(10*index))
                current=cv2.circle(frame1, dot, 2, col, 2)


        for (x, y, w, h) in body1:
            cv2.rectangle(crop_img , (x, y), (x + w, y + h), (0, 255, 0), 2)

        for (x, y, w, h) in body2:
            cv2.rectangle(crop_img, (x, y), (x + w, y + 4*h), (0, 255, 0), 2)

        for (x, y, w, h) in body3:
           cv2.rectangle(crop_img, (x, int(y-h)), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(frame1, "people count: {}".format(count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 3)



    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()