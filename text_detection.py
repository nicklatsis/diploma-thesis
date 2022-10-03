import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time



#img=cv2.imread('2.png')
reader = easyocr.Reader(['en'],gpu=True)
vid =cv2.VideoCapture(0)
skip_frame=True



def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

while(True):
    a=time.time()
    ret,img=vid.read()

    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    result=reader.readtext(gray)
    #result=reader.readtext(gray, detail=0,paragraph=True, y_ths=0.1, x_ths=0.1,text_threshold=0.9)
    text=" "

    for (bbox,text,prob) in result:

        
        #text += result[1] + " "
        print("[INFO] {:.4f}: {}".format(prob, text))

        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        text = cleanup_text(text)
        cv2.rectangle(img, tl, br, (0, 255, 0), 2)
        cv2.putText(img, text, (tl[0], tl[1] - 10),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)

       


    #cv2.putText(img,text,(58,78),cv2.FONT_HERSHEY_SIMPLEX,1,(58,58,255),2)


    #FPS
    b=time.time()
    fps=1/(b-a)
    cv2.line(img,(28,25),(127,25),[85,45,255],30)
    cv2.putText(img,f'FPS:{int(fps)}',(11,35),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,lineType=cv2.LINE_AA)
    cv2.imshow("result",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(fps)
    print(text)




#top_left = tuple(result[0][0][0])
#bot_right=tuple(result[0][0][2])
#text=result[0][1]
#font=cv2.FONT_HERSHEY_COMPLEX

#img=cv2.imread(imgpath)
#img=cv2.rectangle(img,top_left,bot_right,(0,255,0),3)
#img=cv2.putText(img,text,top_left,font, .5,(255,0,0),cv2.LINE_AA)

#plt.imshow(img)
#plt.show()

