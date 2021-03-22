# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 22:13:11 2021

@author: jkescher
"""
import cv2
import numpy as np

def RemoveBG(ImgAve,name,record=False,ContrastTreshold=100,filename='FilteredPIV.avi'):
    video=cv2.VideoCapture(name)
    success,image=video.read()
    height,width,channels=image.shape
    fps=video.get(cv2.CAP_PROP_FPS)
    #read video and find dimensions and properties
    
    if record:
        ymin=0
        xmin=0
        ymax=1080
        ymax=max(ymax,height)
        xmax=1920
        xmax=max(xmax,width)
        videoFile=cv2.VideoWriter(filename,0,fps,(xmax-xmin,ymax-ymin))
        #Defining the dimensions of the frame to be investigated.
        while success:
            ContrastMap=(((image-ImgAve)[:,:,0]>ContrastTreshold)+((image-ImgAve)[:,:,1]>ContrastTreshold)+((image-ImgAve)[:,:,2]>ContrastTreshold)).astype(np.uint8)*255
            ContrastImg=cv2.merge([ContrastMap,ContrastMap,ContrastMap])
            #making a map of where the contrast between the average value and the current picture
            #exceeds the desired contrast threshold.
            videoFile.write(np.clip((ContrastImg)[ymin:ymax,xmin:xmax],0,255).astype(np.uint8))
            success, image=video.read()
            #Writing frame to video and reading new frame
        videoFile.release()
    else:
        ContrastMap=(((image-ImgAve)[:,:,0]>ContrastTreshold)+((image-ImgAve)[:,:,1]>ContrastTreshold)+((image-ImgAve)[:,:,2]>ContrastTreshold)).astype(np.uint8)*255
    cv2.destroyAllWindows()
    return ContrastMap
    #cleaning up the mess we made.