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
        for j in range(contrastMap.shape[1]):
            if contrastMap[i,j]:
                for checkKey in clusters:
                    if (i,j) in clusters[checkKey]["candidate"]:
                        clusters[checkKey]["member"].append((i,j))
                        clusters[checkKey]["candidate"].remove((i,j))
                        for addset in [(i+1,j),(i,j+1),(i+1,j+1)]:
                            clusters[checkKey]["candidate"].add(addset)
                else:
                    clusters[key]={"member":[(i,j)],"candidate":{(i+1,j),(i,j+1),(i+1,j+1)}}
                    key+=1
    return clusters