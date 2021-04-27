# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:15:49 2021

@author: jkescher
"""

def crossCorelateMaps(mainMap,kernel):
    import numpy as np
    normalizationFactor=max([abs(mainMap).max(),abs(kernel.max()),1])
    mainMap=mainMap/normalizationFactor
    kernel=kernel/normalizationFactor#Normalizing the image and the kernel to themselsves
    #emptyMap=np.zeros(mainMap.shape)
    ki=kernel.shape[0]
    kj=kernel.shape[1]
    iImg=mainMap.shape[0]
    jImg=mainMap.shape[1]
    inum=iImg+ki-1#Number of i-values
    jnum=jImg+kj-1#number of j-values to iterate over
    correlation=np.zeros([inum,jnum])
#    for i in range(inum):
#        for j in range(jnum):
#            #The indices don't work as expected, for some reason. I think the sub Map is one step to far?
#            subMap=mainMap[i:i+ki,j:j+kj]
#            print('SubMap',subMap)
#            subMap=subMap[-((ki-1+iImg)-i):i+1,-((kj-1+jImg)-j):j+1]
#            print('Kernel',kernel[-(i+1):(ki-1+iImg)-i,-(j+1):(kj-1+jImg)-j])
#            correlation[i,j]=sumArray(kernel[-(i+1):(ki-1+iImg)-i,-(j+1):(kj-1+jImg)-j]*subMap)#at some point, the size of the sub  map stops increasing,but the kernel size continues on...
    #Trying brute-force zero-padding:
    #I think this works, but it takes extremely long time for just one image... Should really attempt the above way.
    #Should also try to write this for multiprocessing purposes, to process each picture individually.
    #AND, should reduce the image size. big parts are to fuzzy to get a good flow field anyways.
    canvas=np.zeros([inum+ki-1,jnum+kj-1])
    canvas[ki-1:ki+iImg-1,kj-1:kj+jImg-1]=mainMap
    end=float(inum)*float(jnum)
    for i in range(inum):
        for j in range(jnum):
#            print(i,j)
#            print('canvas',canvas[i:i+ki,j:j+kj])
            correlation[i,j]=sumArray(kernel*canvas[i:i+ki,j:j+kj])
            if j % 100 == 0:
                current=float(i)*float(jnum)+float(j)
                print(str(current/end*100)+' %')#To give an indication of the process.
    return correlation

def sumArray(array):
    from collections.abc import Iterable
    arrayOut=array
    while isinstance(arrayOut,Iterable):
        arrayOut=sumArray(sum(array))
    return arrayOut

#should return element index of upper left corner of all discrete elements, as well as height and width of all elements.
    #numel is the number of elements in the vertical direction.
    #If the Map is not exactly one integer amount of element length in every direction, the map will be cropped at the lower and rightmost edges.
def discretizeMap(Map,numel0):
    import copy as cp
    pixels0=int(Map.shape[0]/numel0)
    pixels1=cp.deepcopy(pixels0)
    indexList=[]
    i=0
    j=0
    numel1=int(Map.shape[0]/pixels1)
    while i<=Map.shape[0]-pixels0:
        while j<=Map.shape[1]-pixels1:
            indexList.append((i,j))
            j+=pixels1
        i+=pixels0
        j=0
    return[indexList,pixels0,pixels1,numel0,numel1]

#Applies cross correlation from one picture divided into equally large elements, to another picture to see the change in location

#Errors: Where to begin? the indexList outputs more indices than the size of the displacementX or the displacementY (at least for a 3*3 array).
    #Also, the function does not work, but bluntly pasting it into the command prompt works (better)... wth is this?
def crossCorelateFrames(frame0,numel,frame1):
    import numpy as np
    import copy as cp
    DiscreteProperties=discretizeMap(frame0,numel)#returning the number of pixels in each cell, as well as the number of cells in each direction
    indexList=DiscreteProperties[0] #Puttuing these values in a more readable form:
    pixels0=DiscreteProperties[1]
    pixels1=DiscreteProperties[2]
    numel0=DiscreteProperties[3]
    numel1=DiscreteProperties[4]
    displacementX=np.zeros([numel0,numel1])#initializing a map to write the values for the displacement
    displacementY=cp.deepcopy(displacementX)#Finds max value for current cell corelation on entire canvas.
    icount=0
    jcount=0
    for (i,j) in indexList:
        correlation=crossCorelateMaps(frame1,frame0[i:i+pixels0,j:j+pixels1])
        #correlation=[1,1]
        maxCorelationIndex=np.unravel_index(correlation.argmax(),correlation.shape)#Finds position for upper left corner of frame with best correlation
        displacementX[icount,jcount]=maxCorelationIndex[0]-i+pixels0-1#max index minus i to find displacement, plus (pixels0-1) to adjust for map being larger than canvas
        displacementY[icount,jcount]=maxCorelationIndex[1]-j+pixels1-1
        icount+=1
        if icount>numel0: #Move to next row if we're finished with all indices for current column
            icount=0
            jcount+=1
    return displacementX,displacementY
    
