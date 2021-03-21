# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:25:29 2021

@author: jkescher
"""

# script to filter out bacground from static video
#This gives the mean values of all of the images, but I apparently have no idea of how colours nad stuff works...
#Now the filter works, kinda... But I fear that my webcam does not have good enough resolution for PIV :-(
import cv2
import matplotlib.pyplot as plt
import copy as cp
import numpy as np

record=True
video=cv2.VideoCapture('PIV2.mp4')
success, image=video.read()#to initialize the image_mean file
CalibrationImg=cp.deepcopy(image)
image_sum=image.astype(float)
success, image=video.read()#To have a new image file to add to the mean
counter=1

while success:
    counter+=1
    image_sum+=image
    success,image=video.read()#read new image

ImgAve=(image_sum/counter).astype(int)
plt.imshow(ImgAve)
#The window of interest(So without apparent disturbances) is img[:600,250:1200]
video=cv2.VideoCapture('PIV2.mp4')

success,image=video.read()
height,width,channels=image.shape
ymin=0
xmin=0
ymax=1080
ymax=max(ymax,height)
xmax=1920
xmax=max(xmax,width)
ContrastTreshold=100
videoFile=cv2.VideoWriter('Testvid.avi',0,20,(xmax-xmin,ymax-ymin))
#plt.imshow(image-ImgAve)

while success and record:
    ContrastMap=(((image-ImgAve)[:,:,0]>ContrastTreshold)+((image-ImgAve)[:,:,1]>ContrastTreshold)+((image-ImgAve)[:,:,2]>ContrastTreshold)).astype(np.uint8)*255
    ContrastImg=cv2.merge([ContrastMap,ContrastMap,ContrastMap])
    videoFile.write(np.clip((ContrastImg)[ymin:ymax,xmin:xmax],0,255).astype(np.uint8))
    success, image=video.read()
cv2.destroyAllWindows()
videoFile.release()