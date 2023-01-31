import pygame
import cv2
import math 
import time
from utils import scale_image, blit_rotate_center, stackimages
import keyboard
import numpy as np
import sys
from tkinter import *

pygame.font.init()

screen= Tk()
screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

numOfArgs = len(sys.argv)
map = 0
if numOfArgs>1:
    map = int(sys.argv[1])


if map==0:
    WHITE=(255, 255, 255)
    FPS = 15
    GRASS= scale_image(pygame.image.load('grass.jpg'), 2.6)
    TRACK= scale_image(pygame.image.load('track2.png'), 1.15)
    TRACK_BORDER= scale_image(pygame.image.load('track-border2.png'), 1.15)
    TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)
    START_POS=(690,580)
    CAR= scale_image(pygame.image.load('red-car.png'),0.6) 
    FINISH= pygame.image.load('finish.png')
    FINISH_MASK=pygame.mask.from_surface(FINISH)
    FINISH_PO=(650,630)

    SELF_VEL=100
    ROTATION_VEL=15

    WINNER_FONT= pygame.font.SysFont('comicsans',100)
    WIDTH,HEIGHT= TRACK.get_width(),TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))

elif map==1:
    WHITE=(255, 255, 255)
    FPS = 15
    GRASS= scale_image(pygame.image.load('grass.jpg'), 2.5)
    TRACK= scale_image(pygame.image.load('track.png'), 0.9)
    TRACK_BORDER= scale_image(pygame.image.load('track-border.png'), 0.9)
    TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)
    START_POS=(180,200)
    CAR= scale_image(pygame.image.load('red-car.png'),0.5)
    FINISH= pygame.image.load('finish.png')
    FINISH_MASK=pygame.mask.from_surface(FINISH)
    FINISH_PO=(130,250)
    
    SELF_VEL=100
    ROTATION_VEL=20

    TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)
    WINNER_FONT= pygame.font.SysFont('comicsans',100)
    WIDTH,HEIGHT= TRACK.get_width(),TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))

elif map==2:
    WHITE=(255, 255, 255)
    FPS = 15
    GRASS= scale_image(pygame.image.load('grass.jpg'), 2.6)
    TRACK= scale_image(pygame.image.load('track3.png'), 1.9)
    TRACK_BORDER= scale_image(pygame.image.load('track-border3.png'), 1.9)
    TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)
    START_POS=(720,580)
    CAR= scale_image(pygame.image.load('red-car.png'),0.6)
    FINISH= pygame.image.load('finish.png')
    FINISH_MASK=pygame.mask.from_surface(FINISH)
    FINISH_PO=(680,630)
    
    

    WINNER_FONT= pygame.font.SysFont('comicsans',100)
    WIDTH,HEIGHT= TRACK.get_width(),TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Track Race Game")

elif map==3:
    WHITE=(255, 255, 255)
    FPS = 15
    GRASS= scale_image(pygame.image.load('grass.jpg'), 2.6)
    TRACK= scale_image(pygame.image.load('track4.png'), 1.9)
    TRACK_BORDER= scale_image(pygame.image.load('track-border4.png'), 1.9)
    CAR= scale_image(pygame.image.load('red-car.png'),0.6)
    FINISH= scale_image(pygame.image.load('finish.png'),1.3)
    FINISH_MASK=pygame.mask.from_surface(FINISH)
    FINISH_PO=(730,630)

    START_POS=(790,580)
    TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)

    WINNER_FONT= pygame.font.SysFont('comicsans',100)
    WIDTH,HEIGHT= TRACK.get_width(),TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Track Race Game")

else:
    exit()        

pygame.display.set_caption("Track Race Game")

fWidth=640
fHeight=480
cap = cv2.VideoCapture(0)

cap.set(3,fWidth)
cap.set(4,fHeight)


def empty(a):
    pass


cv2.namedWindow("Parameters")
cv2.moveWindow("Parameters", screen_width-640, screen_height-240)
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
            #cv2.putText(imgContour,"Points:" + str(len(approx)),(x+w+20,y+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
            #cv2.putText(imgContour,"Area:" + str(int(area)),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)

    return shapeList, shapeListPos

class AbstractCar:      #image rotation 
    def __init__(self, max_vel,rotation_vel): 
        self.img=self.IMG
        self.max_vel= max_vel
        self.vel=0
        #self.rotation_vel = rotation_vel
        self.angle=0
        self.x,self.y=self.START_POS
        self.acceleration=1

    def rotate(self,left=False,right=False):
        if left:
          self.angle -= ROTATION_VEL
        elif right:
            self.angle += ROTATION_VEL

    def draw (self, win):
        blit_rotate_center(win, self.img,(self.x,self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel+self.acceleration,self.max_vel)                         #if we reach the higher  acceleration we dont want to pass the max vel
        self.move()

    def move_backward(self):
        self.vel = max(self.vel-self.acceleration,-self.max_vel/2) 
        self.move()
    

    def move(self):                                                                   #basic trigonometry for direction of the movement of the cr
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel 
        horizontal= math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self) :
        self.vel = max(self.vel-self.acceleration,0) #if this value is negative we dont want to go backards but to stop
        self.move()

    def collision(self,mask,x=0,y=0): #masks
        car_mask=pygame.mask.from_surface(self.img)
        offset=(int(self.x-x),int(self.y-y))
        poi=mask.overlap(car_mask,offset)  #point of intersection
        #the calling mask (car) is the one to compare ith the other mask 
        return poi
    
    def reset(self):
        self.x,self.y=START_POS
        self.vel=0
        self.angle=0




class PlayerCar(AbstractCar):
    
    IMG= CAR
    if map==1:
        START_POS=(180,200)
    elif map==0:
        START_POS=(690,580)  
    elif map==2:
        START_POS=(720,580) 
    elif map==3:
        START_POS=(790,580)
    #VEL=5
    #ANGLE=30
    def bounceback(self):
        self.vel= -self.vel # reverces the velocities so if e go front bounce back and the other arroud
        self.move()
    



def draw(win,images,car):
    for img,pos in images:
        win.blit(img,pos)  
    car.draw(win)

    pygame.display.update()


    
#def move_car(car,sortedInstructions):
    #keys=pygame.key.get_pressed() 
    #moved=False # if we press w we dont want reduced speed but if we let go we do want 

    #if keys[pygame.K_RIGHT]:
        #car.rotate(left=True)
    #if keys[pygame.K_LEFT]:
        #car.rotate(right=True)
    #if keys[pygame.K_UP]:
        #moved=True
        #car.move_forward()
    #if keys[pygame.K_DOWN]:
        #moved=True
        #car.move_backward()
    


def draw_winner(text):
    draw_text=WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



run=True
clock=pygame.time.Clock()
images=[(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,FINISH_PO), (TRACK_BORDER,(0,0))]
car=PlayerCar(4,4)

checkIfInstructionsChangedEvery = 5
prevInstructions = []
instructionsChangedAt = int( time.time() )

waitForSettings =  int( time.time() )

hasRunned = False


while run:
    success,img= cap.read()
    
    imgContour=img.copy()
    clock.tick(FPS)
    keys=pygame.key.get_pressed() 


    cv2.resizeWindow
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break

    imgBlur = cv2.GaussianBlur(img,(7,7),1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    

    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")
    
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
   
    kernel=np.ones((5,5))

    imgDil = cv2.dilate(imgCanny,kernel, iterations=1)

    instructions, instructionOrder = getContours(imgDil,imgContour)

    tmpInstructions = instructions


    if int( time.time() ) - instructionsChangedAt > checkIfInstructionsChangedEvery:
        print("<<<<<<<<<<<<<<<<<<<<<CHANGED>>>>>>>>>>>>>>>>>>>")
        prevInstructions = instructions
        instructionsChangedAt = int( time.time() )
        hasRunned = False

    
    if set(tmpInstructions) == set(prevInstructions) and len(instructions) and int( time.time() ) - instructionsChangedAt > 3 and int( time.time() ) - waitForSettings > 20 and not hasRunned:
        print("running...")
        hasRunned = True
        sortedInstructions = [x for y,x in sorted(zip(instructionOrder,instructions))]
        for shape in sortedInstructions:
            if shape=='Arrow':
                moved=True
                for i in range(5):
                    if car.collision(TRACK_BORDER_MASK) != None:
                        break
                    else:
                        car.move_forward()
                
            if shape=='Rectangle':
                moved=True
                if car.collision(TRACK_BORDER_MASK) != None:
                        break
                else:
                    car.rotate(right=True)
                
            if shape=='Circle':
                moved=True
                if car.collision(TRACK_BORDER_MASK) != None:
                    break
                else:
                    car.rotate(left=True)
                
            if shape=='Triangle':
                moved=True
                for i in range(10):
                    if car.collision(TRACK_BORDER_MASK) != None:
                        break
                    else:
                        car.move_backward()
                
            if not moved:
               car.reduce_speed()   

            time.sleep(1)
                  
         


    imgStack= stackimages(0.7,([imgContour,img,imgCanny]))
 
    

    #move_car(car)
    draw(WIN,images,car)

    if car.collision(TRACK_BORDER_MASK) != None:
        car.bounceback()
    finishX, finishY = FINISH_PO
    finish_poi_collide=car.collision(FINISH_MASK, finishX, finishY)
    if finish_poi_collide != None: 
        if finish_poi_collide[1]==0:
           car.bounceback() 
        else:
            car.reset()
            winner_text=""
            winner_text="YOU WIN"
            if winner_text != "" :
                draw_winner(winner_text)
            break



    cv2.imshow("camera feed",imgStack)
    cv2.moveWindow("camera feed", 0,0)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break


pygame.quit()

