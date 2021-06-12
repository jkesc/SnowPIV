# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""
#To do:
#It seems like some parts get larger values at false locations. probably because the range is fuzzy(not 1 or 0). Should make it either snowflake or noflake, in order to avoid this.
#Have to be able to actually compare two and two frames. Extend the GetContrast file to enable you to do so.
#main function
import FilterBG as FBG
import GetContrast as GC
#import FindCluster as FC
import CrossCorelation as CC

def main():
    BG=FBG.GetBG('PIV2.mp4')
    i=100
    contrastMap=GC.RemoveBG(BG,'PIV2.mp4',False,i,str(i)+'.avi')
    #clusters=FC.getClusters(contrastMap)
    #FC.colorCluster(clusters,contrastMap)
    #CorelationMap=CC.crossCorelateMaps(contrastMap,contrastMap[5:500,7:502])
    dx,dy,idx=CC.crossCorelateFrames(contrastMap[0:400,250:650],10,contrastMap[5:405,255:655],True)
    return [contrastMap,BG,dx,dy,idx]#, CorelationMap]#CorelationMap

if __name__=="__main__":
#    contrastMap, clusters, BG=main()
    ValOut=main()
    #Find the average value of all of the images and return it.
