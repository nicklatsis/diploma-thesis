import  cv2
import numpy as np
import keyboard

frameWidth = 640
frameHeight= 400
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)


def stackimages(scale,imgArray):
    rows=len(imgArray)
    cols=len(imgArray[0])
    rowsAvailable= isinstance(imgArray[0],list)
    width= imgArray[0][0].shape[1]
    height= imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0,rows):
            for y in range(0,cols):
                if imgArray[x][y].shape[:2]==imgArray[0][0].shape[:2]:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y]=cv2.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)
                if len(imgArray[x][y].shape)==2: imgArray[x][y]=cv2.cvtColor(imgArray[x][y],cv2.COLOR_BAYER_BG2BGR)
        imageBlanck = np.zeros((height,width,3),np.uint8)
        hor =[imageBlanck]*rows
        hor_con =[imageBlanck]*rows
        for x in range(0,rows):
            hor[x] = np.hstack(imgArray[x])
        ver= np.vstack(hor)
    else:
        for x in range(0,rows):
            if imgArray[x].shape[:2] ==imgArray[0].shape[:2]:
                imgArray[x]=cv2.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x]=cv2.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape)==2 : imgArray[x]=cv2.cvtColor(imgArray[x],cv2.COLOR_GRAY2BGR)  
        hor=np.hstack(imgArray)
        ver=hor
    return ver
        


def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)


def getContours(img,imgContour):

    contours, hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    shapeList = []
    shapeListPos = []

    for cnt in contours:
        area=cv2.contourArea(cnt)
        areamin=cv2.getTrackbarPos("Area","Parameters")
        if area > areamin:
            cv2.drawContours(imgContour,cnt, -1,(255,0,255),7)
            peri=cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
            #print(len(approx))
            x,y,w,h=cv2.boundingRect(approx)

            if len(approx)==3:
                cv2.putText(imgContour,"Triangle",(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                shapeList.append("Triangle")
                shapeListPos.append(x)
            elif len(approx)==4:
                cv2.putText(imgContour,"Rectangle",(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                shapeList.append("Rectangle")
                shapeListPos.append(x)
            elif len(approx)==7:
                cv2.putText(imgContour,"Arrow",(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                shapeList.append("Arrow")
                shapeListPos.append(x)
            elif 8 >= len(approx):
                cv2.putText(imgContour,"Circle",(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                shapeList.append("Circle")
                shapeListPos.append(x)

            
            cv2.rectangle(imgContour,(x, y),(x+w,y+h),(0,255,0),5)
            cv2.putText(imgContour,"Points:" + str(len(approx)),(x+w+20,y+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
            #cv2.putText(imgContour,"Area:" + str(int(area)),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)

    return shapeList, shapeListPos


while True:
    success,img= cap.read()
    imgContour=img.copy()


    imgBlur = cv2.GaussianBlur(img,(7,7),1)
    #blank_image = np.zeros_like(threslold_image)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    #img_canny = cv2.Canny(img_gray,threshold1, 50, 50)
    #kernel = np.ones((3, 3))
    #img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    #img_erode = cv2.erode(img_dilate, kernel, iterations=1)


    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)

    kernel=np.ones((5,5))

    imgDil = cv2.dilate(imgCanny,kernel, iterations=1)

    instructions, instructionOrder = getContours(imgDil,imgContour)

    if keyboard.is_pressed('a'):  
        sortedInstructions = [x for y,x in sorted(zip(instructionOrder,instructions))]


    imgStack= stackimages(0.8,([img,imgGray,imgCanny],[imgDil,imgContour,imgContour]))
 

    


    cv2.imshow("result",imgStack)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
