import pygame 
import math 
import time
from utils import scale_image, blit_rotate_center
pygame.font.init()

WHITE=(255, 255, 255)
FPS = 60
GRASS= scale_image(pygame.image.load('grass.jpg'), 2.5)
TRACK= scale_image(pygame.image.load('track.png'), 0.9)
TRACK_BORDER= scale_image(pygame.image.load('track-border.png'), 0.9)
CAR= scale_image(pygame.image.load('red-car.png'),0.5)
FINISH= pygame.image.load('finish.png')
FINISH_MASK=pygame.mask.from_surface(FINISH)


TRACK_BORDER_MASK=pygame.mask.from_surface(TRACK_BORDER)
WINNER_FONT= pygame.font.SysFont('comicsans',100)
WIDTH,HEIGHT= TRACK.get_width(),TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Track Race Game")


class AbstractCar:      #image rotation 
    def __init__(self, max_vel,rotation_vel): 
        self.img=self.IMG
        self.max_vel= max_vel
        self.vel=0
        self.rotation_vel = rotation_vel
        self.angle=0
        self.x,self.y=self.START_POS
        self.acceleration=0.1

    def rotate(self,left=False,right=False):
        if left:
          self.angle -= self.rotation_vel+3
        elif right:
            self.angle += self.rotation_vel+3

    def draw (self, win):
        blit_rotate_center(win, self.img,(self.x,self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel+self.acceleration,self.max_vel) #if we reach the higher  acceleration we dont want to pass the max accel
        self.move()

    def move_backward(self):
        self.vel = max(self.vel-self.acceleration,-self.max_vel/2) 
        self.move()
    

    def move(self): #basic trigonometry for direction of the movement of the cr
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal= math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self) :
        self.vel = max(self.vel-self.acceleration,0) #if this value is negative e dont ant to go backards but to stop
        self.move()

    def collision(self,mask,x=0,y=0): #masks
        car_mask=pygame.mask.from_surface(self.img)
        offset=(int(self.x-x),int(self.y-y))
        poi=mask.overlap(car_mask,offset)  #point of intersection
        #the calling mask (car) is the one to compare ith the other mask 
        return poi



class PlayerCar(AbstractCar):
    
    IMG= CAR
    START_POS=(180,200)
    def bounceback(self):
        self.vel= -self.vel # reverces the velocities so if e go front bounce back and the other arroud
        self.move()
    



def draw(win,images,car):
    for img,pos in images:
        win.blit(img,pos)
    
       
    car.draw(win)

    pygame.display.update()


    
def move_car(car):
    keys=pygame.key.get_pressed() 
    moved=False # if we press w we dont want reduced speed but if we let go we do want 

    if keys[pygame.K_RIGHT]:
        car.rotate(left=True)
    if keys[pygame.K_LEFT]:
        car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved=True
        car.move_forward()
    if keys[pygame.K_DOWN]:
        moved=True
        car.move_backward()
    
    if not moved:
        car.reduce_speed()

def draw_winner(text):
    draw_text=WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

run=True
clock=pygame.time.Clock()
images=[(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,(130,250)), 
        (TRACK_BORDER,(0,0))]
car=PlayerCar(4,4)

while run:
    clock.tick(FPS)
    draw(WIN,images,car)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break

    move_car(car)

    if car.collision(TRACK_BORDER_MASK) != None:
        car.bounceback()
    
    finish_poi_collide=car.collision(FINISH_MASK,130,250)
    if finish_poi_collide != None: 
        if finish_poi_collide[1]==0:
           car.bounceback() 
        else:
            winner_text=""
            winner_text="YOU WIN"
            if winner_text != "" :
                draw_winner(winner_text)
            break


pygame.quit()