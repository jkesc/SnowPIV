# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""

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
    CC.crossCorelateFrames(contrastMap[0:400,250:650],10,contrastMap[0:400,250:650])
    return [contrastMap,BG]#, CorelationMap]#CorelationMap

if __name__=="__main__":
#    contrastMap, clusters, BG=main()
    ValOut=main()
    #Find the average value of all of the images and return it.
