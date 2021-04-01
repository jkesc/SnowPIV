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
    return contrastMap,clusters,BG



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
                clusters[key]={"member":{(i,j)},"candidate":{(i+1,j),(i,j+1),(i+1,j+1)}}#else, make entry for new subset and increas key by 1
                keyChain=list()
                for checkKey in clusters: #Checking the "clusters" dict to see if this point is part of another cluster
                    if (i,j) in clusters[checkKey]["candidate"] and key != checkKey: #if it is, add the older cluster to this new one, and delete the older one
                        clusters[key]["member"] |= clusters[checkKey]["member"]
                        clusters[key]["candidate"] |= clusters[checkKey]["candidate"]
                        keyChain.append(checkKey)
                for k in keyChain:
                    del clusters[k]
                key+=1
    return clusters

#This one just checks the size of each cluster, and colors it according to its size.
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

def getClusterdims(clusters,name="member"): #Used for debugging only
    a=[]
    for l in clusters:
        a.append(len(clusters[l][name]))
    print(max(a))

#I Don't understand how this FFT business works...
def crossCorelateMaps(mainMap,kernel):
    import numpy as np
    mainMap=mainMap/abs(mainMap).max()
    kernel=kernel/abs(kernel).max()#Normalizing the image and the kernel to themselsves
    # invertedMap=np.flip(np.flip(mainMap,0),1)#Cross correlation is just a convolution with one flipped matrix
    kernel=np.flip(np.flip(kernel,0),1)
    #emptyMap=np.zeros(mainMap.shape)
    ki=kernel.shape[0]
    kj=kernel.shape[1]
    inum=mainMap.shape[0]-ki#Number of i-values
    jnum=mainMap.shape[1]-kj#number of j-values to iterate over
    correlation=np.zeros([inum,jnum])
    for i in range(inum):
        for j in range(jnum):
            subMap=mainMap[i:i+ki,j:j+kj]
            correlation[i,j]=sum(sum(np.fft.ifft2(np.fft.fft2(kernel)*np.fft.fft2(subMap))))
    return correlation

if __name__=="__main__":
    contrastMap, clusters, BG=main()
    #Find the average value of all of the images and return it.
