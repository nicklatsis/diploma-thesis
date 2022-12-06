import pygame
import cv2
import numpy as np

def scale_image(img,factor):
    size=round(img.get_width()*factor), round(img.get_height()*factor) #we need int not dec to scale the image so we round it
    return pygame.transform.scale(img,size)

def blit_rotate_center(win,image,top_left,angle):
    rotated_image = pygame.transform.rotate(image,angle)
    new_rect=rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image,new_rect.topleft)

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
        for x in range(0,rows):
            hor[x] = np.vstack(imgArray[x])
        ver= np.hstack(hor)
    else:
        for x in range(0,rows):
            if imgArray[x].shape[:2] ==imgArray[0].shape[:2]:
                imgArray[x]=cv2.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x]=cv2.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape)==2 : imgArray[x]=cv2.cvtColor(imgArray[x],cv2.COLOR_GRAY2BGR)  
        ver=np.vstack(imgArray)
        hor=ver
    return ver