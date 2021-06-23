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
def colorCluster(cluster,contrastMap,sizeMin=17,sizeMax=200,colorInRange=255,colorOutsideRange=255):
    import copy as cp
    R=cp.deepcopy(contrastMap)
    G=cp.deepcopy(contrastMap)
    B=cp.deepcopy(contrastMap)
    for key in cluster:
        #color=key%255
        for i in cluster[key]["member"]:
            if len(cluster[key]["member"])>sizeMin and len(cluster[key]["member"])<sizeMax:
                R[i]=colorInRange
                G[i]=0
            else:
                G[i]=colorOutsideRange
                R[i]=0
            B[i]=0
    return R,G,B




def getClusterdims(clusters,name="member"): #Used for debugging only
    a=[]
    for l in clusters:
        a.append(len(clusters[l][name]))
    print(max(a))