# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""

#main function
#import FilterBG as FBG
#import GetContrast as GC
#import FindCluster as FC
def main():
    BG=GetBG('PIV2.mp4')
    i=100
    contrastMap=RemoveBG(BG,'PIV2.mp4',False,i,str(i)+'.avi')
    clusters=getClusters(contrastMap)
    colorCluster(clusters,contrastMap)
    return contrastMap,clusters



#Current plan: make dictionary of dictionarys.
#Each entry has two sets: possible candidates and members.
#For each index that is truue: check if it is already in a possible candidates. If it is, pop that entry from the possible candidates and add it to the members list.
#If the True entry is not in a list, make a new dictionary wit a key incremented by one.
#In any case, add (i+1,j),(i,j+1 and i+1,j+1) to the list of possible candidates for this elements cluster.
def getClusters(contrastMap):
    key=0
    clusters={}
    for i in range(contrastMap.shape[0]):
        for j in range(contrastMap.shape[1]): #Iterate through entire image
            if contrastMap[i,j]: #only have to do something if the pixel is true
                for checkKey in clusters:#Checking the "clusters" dict to see if this point is part of another cluster
                    if (i,j) in clusters[checkKey]["candidate"]:#if it is, add it to the right cluster and remove from candidate list
                        clusters[checkKey]["member"] |= {(i,j)}
                        clusters[checkKey]["candidate"].remove((i,j))                       
                        clusters[checkKey]["candidate"] |= {(i+1,j),(i,j+1),(i+1,j+1)}#Add unchecked neighboring cells to candidate list
                else:
                    clusters[key]={"member":{(i,j)},"candidate":{(i+1,j),(i,j+1),(i+1,j+1)}}#else, make entry for new subset and increas key by 1
                    key+=1
    return clusters

#The next one uses much time and does absoluetely nothing...
def joinClusters(ClusterDict):
    for key in ClusterDict:
        for compareKey in ClusterDict:
            if compareKey != key:
                if not ClusterDict[key]["member"].isdisjoint(ClusterDict[compareKey]["member"]):
                    ClusterDict[key]["member"] |= ClusterDict[compareKey]["member"]
    return ClusterDict

#This one just checks the size f each cluster, and colors it according to its size.
def colorCluster(cluster,contrastMap,size=17,colorAbove=255,colorBelow=255):
    import copy as cp
    R=cp.deepcopy(contrastMap)
    G=cp.deepcopy(contrastMap)
    B=cp.deepcopy(contrastMap)
    for key in cluster:
        #color=key%255
        for i in cluster[key]["member"]:
            if len(cluster[key]["member"])>size:
                R[i]=colorAbove
                G[i]=0
            else:
                G[i]=colorBelow
                R[i]=0
            B[i]=0
    return R,G,B

def RemoveBG(ImgAve,name,record=False,ContrastTreshold=100,filename='FilteredPIV.avi'):
    import cv2
    import numpy as np
    
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

# script to filter out bacground from static video
#This gives the mean values of all of the images, but I apparently have no idea of how colours nad stuff works...
#Now the filter works, kinda... But I fear that my webcam does not have good enough resolution for PIV :-(
import matplotlib.pyplot as plt
def GetBG(name):
    import cv2
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

if __name__=="__main__":
    contrastMap, clusters=main()
    #Find the average value of all of the images and return it.