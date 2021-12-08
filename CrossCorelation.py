# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:15:49 2021

@author: jkescher
"""
#To do:
#Find out why the discretizeMap function sometimes spits out a too large value for numel1. Maybe something related to rounding errors?
#Should also make a statement where parts with only zero in them get a velocity change of zero.

#This seems to spit out what I expected, but is hopelessly insufficient compared to opencv2...
def crossCorelateMaps(mainMap,kernel,Progress=False):
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
    #I think this works, but it takes extremely long time for just one image... Should really attempt a way without the zeros around...
    #Should also try to write this for multiprocessing purposes, to process each picture individually.
    #AND, should reduce the image size. large parts of it are to fuzzy to get a good flow field anyways.
    canvas=np.zeros([inum+ki-1,jnum+kj-1])
    canvas[ki-1:ki+iImg-1,kj-1:kj+jImg-1]=mainMap
    end=float(inum)*float(jnum)
    for i in range(inum):
        for j in range(jnum):
            correlation[i,j]=sumArray(kernel*canvas[i:i+ki,j:j+kj])
            if j % 100 == 0 and Progress == True:
                current=float(i)*float(jnum)+float(j)
                print(str(current/end*100)+' %')#To give an indication of the process.
    return correlation

def crossCorelateFramesCV2(frame0,numel,frame1,Progress=False):
    
    import numpy as np
    import copy as cp
    import cv2

    numel_max=min(frame0.shape[0],frame0.shape[1])#failsafe in case somebody inputs a numel larger than the frame size.
    if numel>numel_max:
        from inspect import currentframe, getframeinfo #Copied this from the internet somewhere, gives filename and line number
        cf = currentframe()
        filename = getframeinfo(cf).filename
        numel=numel_max #sets numel to smallest frame size
        print('Warning: numel changed to '+str(numel_max)+' in file '+str(filename)+', line '+str(cf.f_lineno)+'\n') #tells user about what was done
        
    DiscreteProperties=discretizeMap(frame0,numel)#returning the number of pixels in each cell, as well as the number of cells in each direction
    
    indexList=DiscreteProperties[0] #Putting these values in a more readable form:
#    print(indexList)
    pixels0=DiscreteProperties[1]#pixels in 0 dirn
    pixels1=DiscreteProperties[2]#pixels in 1 dirn
#    print('\npixels 0: '+str(pixels0)) 
#    print('\npixels 1: '+str(pixels1))
    numel0=DiscreteProperties[3]#elements in 0 dirn
    numel1=DiscreteProperties[4]#elements in 1 dirn
#    print('\nnumel 0: '+str(numel0)) 
#    print('\nnumel 1: '+str(numel1))
    displacementX=np.zeros([numel0,numel1])#initializing a map to write the values for the displacement
    displacementY=cp.deepcopy(displacementX)#Finds max value for current cell corelation on entire canvas.
    
    icount=0
    jcount=0
    if Progress == True:
        iProgress=0
    
    for (i,j) in indexList:
        if Progress == True:
            print(str(iProgress*100/len(indexList))+'%\n')
            iProgress+=1
        correlation=cv2.matchTemplate(frame1,frame0[i:i+pixels0,j:j+pixels1],cv2.TM_CCOEFF)
        maxCorelationIndex=np.unravel_index(correlation.argmax(),correlation.shape)#Finds position for upper left corner of frame with best correlation
#        print('submap:\n'+str(frame0[i:i+pixels0,j:j+pixels1]))
#        print('\ncorrelation:\n'+str(correlation))
#        print('\nmax index: '+str(maxCorelationIndex))
        displacementY[icount,jcount]=-(maxCorelationIndex[0]-i-(pixels0-1))#max index minus i to find displacement, minus (pixels0-1) to adjust for map being larger than canvas
        #dy is inversed as the indexing starts from the top, but cartesian systems start at the bottom. As does "plt.quiver"
        displacementX[icount,jcount]=maxCorelationIndex[1]-j-(pixels1-1)
        
        icount+=1
        if icount>=numel0: #Move to next row if we're finished with all indices for current column
            icount=0
            jcount+=1
    return displacementX,displacementY,indexList

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
    j=0
    numel1=int(Map.shape[0]/pixels1)
    for l in range(numel1): #Iterate through map indices, spaced with pixels1 inbetween in dim 1 and pixels0 in dim 0
        i=0 #restart i for each new j
        for k in range(numel0):
            indexList.append((i,j))
            i+=pixels0
        j+=pixels1
#    while i<=Map.shape[0]-pixels0:
#        while j<=Map.shape[1]-pixels1:
#            indexList.append((i,j))
#            j+=pixels1
#        i+=pixels0
#        j=0
    return[indexList,pixels0,pixels1,numel0,numel1]

#Applies cross correlation from one picture divided into equally large elements, to another picture to see the change in location

#Errors: Where to begin? the indexList outputs more indices than the size of the displacementX or the displacementY (at least for a 3*3 array).
    #Also, the function does not work, but bluntly pasting it into the command prompt works (better)... wth is this?
def crossCorelateFrames(frame0,numel,frame1,Progress=False):
    
    import numpy as np
    import copy as cp

    numel_max=min(frame0.shape[0],frame0.shape[1])#failsafe in case somebody inputs a numel larger than the frame size.
    if numel>numel_max:
        from inspect import currentframe, getframeinfo #Copied this from the internet somewhere, gives filename and line number
        cf = currentframe()
        filename = getframeinfo(cf).filename
        numel=numel_max #sets numel to smallest frame size
        print('Warning: numel changed to '+str(numel_max)+' in file '+str(filename)+', line '+str(cf.f_lineno)+'\n') #tells user about what was done
        
    DiscreteProperties=discretizeMap(frame0,numel)#returning the number of pixels in each cell, as well as the number of cells in each direction
    
    indexList=DiscreteProperties[0] #Putting these values in a more readable form:
#    print(indexList)
    pixels0=DiscreteProperties[1]#pixels in 0 dirn
    pixels1=DiscreteProperties[2]#pixels in 1 dirn
#    print('\npixels 0: '+str(pixels0)) 
#    print('\npixels 1: '+str(pixels1))
    numel0=DiscreteProperties[3]#elements in 0 dirn
    numel1=DiscreteProperties[4]#elements in 1 dirn
#    print('\nnumel 0: '+str(numel0)) 
#    print('\nnumel 1: '+str(numel1))
    displacementX=np.zeros([numel0,numel1])#initializing a map to write the values for the displacement
    displacementY=cp.deepcopy(displacementX)#Finds max value for current cell corelation on entire canvas.
    
    icount=0
    jcount=0
    if Progress == True:
        iProgress=0
    
    for (i,j) in indexList:
        if Progress == True:
            print(str(iProgress*100/len(indexList))+'%\n')
            iProgress+=1
        correlation=crossCorelateMaps(frame1,frame0[i:i+pixels0,j:j+pixels1])
        maxCorelationIndex=np.unravel_index(correlation.argmax(),correlation.shape)#Finds position for upper left corner of frame with best correlation
#        print('submap:\n'+str(frame0[i:i+pixels0,j:j+pixels1]))
#        print('\ncorrelation:\n'+str(correlation))
#        print('\nmax index: '+str(maxCorelationIndex))
        displacementY[icount,jcount]=-(maxCorelationIndex[0]-i-(pixels0-1))#max index minus i to find displacement, minus (pixels0-1) to adjust for map being larger than canvas
        #dy is inversed as the indexing starts from the top, but cartesian systems start at the bottom. As does "plt.quiver"
        displacementX[icount,jcount]=maxCorelationIndex[1]-j-(pixels1-1)
        
        icount+=1
        if icount>=numel0: #Move to next row if we're finished with all indices for current column
            icount=0
            jcount+=1
    return displacementX,displacementY,indexList
    
