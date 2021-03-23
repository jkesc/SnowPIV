# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 21:52:38 2021

@author: jkescher
"""

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
import copy as cp
def colorCluster(cluster,contrastMap,size=17):
    R=cp.deepcopy(contrastMap)
    G=cp.deepcopy(contrastMap)
    B=cp.deepcopy(contrastMap)
    color=255
    for key in cluster:
        #color=key%255
        for i in cluster[key]["member"]:
            if len(cluster[key]["member"])>size:
                R[i]=0
                G[i]=0
            else:
                G[i]=color
                R[i]=0
            B[i]=0
    return R,G,B