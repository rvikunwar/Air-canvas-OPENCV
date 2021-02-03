import numpy as np
import cv2 as cv

def empty():
    pass

capture=cv.VideoCapture(0)

c=1

point=[]
cv.namedWindow("trackbar")
cv.resizeWindow("trackbar",640,240)
draw=np.zeros((600,1200,3),dtype="uint8")+255

cv.createTrackbar("Hue Min","trackbar",92,179,empty)
cv.createTrackbar("Sat Min","trackbar",112,255,empty)
cv.createTrackbar("Val Min","trackbar",163,255,empty)

cv.createTrackbar("Hue Max","trackbar",179,179,empty)
cv.createTrackbar("Sat Max","trackbar",255,255,empty)
cv.createTrackbar("Val Max","trackbar",255,255,empty)
while True:
    get,face=capture.read()
    face=cv.flip(face,1)
        
    image=cv.resize(face,(1200,600))
    imgHSV=cv.cvtColor(image,cv.COLOR_BGR2HSV)
    
    hue_min=cv.getTrackbarPos("Hue Min","trackbar")
    sat_min=cv.getTrackbarPos("Sat Min","trackbar")
    val_min=cv.getTrackbarPos("Val Min","trackbar")
    hue_max=cv.getTrackbarPos("Hue Max","trackbar")
    sat_max=cv.getTrackbarPos("Sat Max","trackbar")
    val_max=cv.getTrackbarPos("Val Max","trackbar")
  

    lower=np.array([hue_min,sat_min,val_min])
    upper=np.array([hue_max,sat_max,val_max])
    
    mask=cv.inRange(imgHSV,lower,upper)
    mask=cv.erode(mask,(3,3),iterations=1)
    mask=cv.morphologyEx(mask,cv.MORPH_OPEN,(3,3))
    mask=cv.dilate(mask,(3,3),iterations=1)
    img_res=cv.bitwise_and(image,image,mask=mask)
    center=None
    cnts,_=cv.findContours(mask.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
   
    if len(cnts)>0:
        cnt=sorted(cnts,key=cv.contourArea,reverse=True)[0]
        ((x,y),radius)=cv.minEnclosingCircle(cnt)
        cv.circle(image,(int(x),int(y)),int(radius),(0,255,255),2)
        
        center=[int(x),int(y)]
        
        
        point.append(center)
        if c==0:
            point.append(center)

        
        if cv.waitKey(2) & 0xFF==ord("w"):
            c=0
            while True:
                print("not")
                if cv.waitKey(2) & 0xFF==ord("w"):
                    break
            
           
        else:
            if radius>10 and len(point)>2:
                cv.line(draw,tuple(point[-1]),tuple(point[-2]),(0,255,0),7)  
                c=1
   
    
    if cv.waitKey(1) & 0xFF==ord("c"):   
        point=[]
        draw=np.zeros((600,1200,3),dtype="uint8")+255
   
    cv.imshow("image",image)
    cv.imshow("draw",draw)
    cv.imshow("original image",imgHSV)
    cv.imshow("masked image",mask)
   
    if cv.waitKey(1) & 0xFF==ord("q"):
        break

    


cv.destroyAllWindows()
