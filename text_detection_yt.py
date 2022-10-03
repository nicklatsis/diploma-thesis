import pytesseract
import cv2


font_scale=1.5
font=cv2.FONT_HERSHEY_PLAIN

video=cv2.VideoCapture(0)
video.set(3,640)
video.set(4,480)

pytesseract.pytesseract.tesseract_cmd='D:\\tessaract\\tesseract.exe'


#img=cv2.imread('1.png')


while True:
    ret,img=video.read()
    himg,wimg,_= img.shape

    #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img=cv2.bilateralFilter(img,11,17,17)
    box1=pytesseract.image_to_boxes(img)
    for a in box1.splitlines():
            a=a.split(" ")
            x,y= int(a[1]),int(a[2])
            w,h=int(a[3]),int(a[4])

            cv2.rectangle(img,(x,himg-y),(w,himg-h),(0,255,0), 2)
            cv2.putText(img,a[0],(x,himg-y+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)



    cv2.imshow('Result',img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
