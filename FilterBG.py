# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:25:29 2021

@author: jkescher
"""
import cv2
# script to filter out bacground from static video
#This gives the mean values of all of the images, but I apparently have no idea of how colours nad stuff works...
#Now the filter works, kinda... But I fear that my webcam does not have good enough resolution for PIV :-(
#import matplotlib.pyplot as plt
def GetBG(name):
    video=cv2.VideoCapture(name)
    success, image=video.read()
    #loading the first frame of the video and making a copy of it for later summing
    image_sum=image.astype(float)
    success, image=video.read()#To have a new image file to add to the mean
    counter=1
    while success:
        counter+=1
        image_sum+=image
        success,image=video.read()
        #read new image and add it to the other images
    
    ImgAve=(image_sum/counter).astype(int)
    return ImgAve