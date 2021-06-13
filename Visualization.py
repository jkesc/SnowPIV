# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 14:45:44 2021

@author: jkescher
"""

#Show results
def vectorField(frame,dx,dy,idx,VectorColor=[0,1,0],frame2=0):
    import matplotlib.pyplot as plt
    import numpy as np
    import cv2
    fig=plt.figure(1)
    if type(frame2)==int:
        plt.imshow(cv2.merge([frame,frame,frame]))
    else:
        plt.imshow(cv2.merge([frame,frame*0,frame2]))
    xVec=np.array([])
    yVec=np.array([])
    for i,j in idx:
        xVec=np.append(xVec,i)
        yVec=np.append(yVec,j)
#    xOffset=abs(xVec[1]-xVec[0])/2
#    yOffset=abs(yVec[1]-yVec[0])/2
#    plt.quiver(xVec+xOffset,yVec+yOffset,dx,dy,color=VectorColor)
    plt.quiver(xVec,yVec,dx,dy,color=VectorColor)
    return fig
    
    