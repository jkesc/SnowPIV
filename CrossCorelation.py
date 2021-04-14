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
    return correlation,canvas

def sumArray(array):
    from collections.abc import Iterable
    arrayOut=array
    while isinstance(arrayOut,Iterable):
        arrayOut=sumArray(sum(array))
    return arrayOut
