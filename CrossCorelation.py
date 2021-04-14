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
                print(current/end)#To give an indication of the process.
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
def crossCorelateFrames(frame0,numel,frame1):
    import numpy as np
    import copy as cp
    DiscreteProperties=discretizeMap(frame0,numel)
    indexList=DiscreteProperties[0]
    pixels0=DiscreteProperties[1]
    pixels1=DiscreteProperties[2]
    numel0=DiscreteProperties[3]
    numel1=DiscreteProperties[4]
    displacement=np.zeros([numel0,numel1])
    canvasIndex=cp.deepcopy(displacement)
    icount=0
    jcount=0
    for (i,j) in DiscreteProperties[0]:
        correlation=crossCorelateMaps(frame1,frame0[i:i+DiscreteProperties[1],j:DiscreteProperties[2]])
        canvasIndex[icount,jcount]=np.unravel_index(correlation.argmax(),correlation.shape)
        displacement[icount,jcount]=(canvasIndex[icount,jcount][0]-i+DiscreteProperties[1]-1,canvasIndex[icount,jcount][1]-j+DiscreteProperties[2]-1)
        icount+=1
        if icount>DiscreteProperties[3]:
            icount=0
            jcount+=1
    return displacement    
        