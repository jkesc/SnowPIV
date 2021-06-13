# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""
#To do:
#It seems like some parts get larger values at false locations. probably because the range is fuzzy(not 1 or 0). Should make it either snowflake or noflake, in order to avoid this.
#main function
import FilterBG as FBG
import GetContrast as GC
#import FindCluster as FC
import CrossCorelation as CC
import Visualization as VS

def main():
    BG=FBG.GetBG('PIV2.mp4')
    threshold=100#contrast threshold
    for i in range(20):
        contrastMap0=GC.RemoveBG(BG,'PIV2.mp4',record=False,ContrastThreshold=threshold,filename=str(threshold)+'.avi',frame=i)
        contrastMap1=GC.RemoveBG(BG,'PIV2.mp4',record=False,ContrastThreshold=threshold,filename=str(threshold)+'.avi',frame=i+1)
        dx,dy,idx=CC.crossCorelateFrames(contrastMap0[0:400,250:650],10,contrastMap1[0:400,250:650],True)
        image=VS.vectorField(contrastMap0[0:400,250:650],dx,dy,idx)
        image.savefig('vectorField_frame_'+str(i)+'.png')
    return [contrastMap0,contrastMap1,BG,dx,dy,idx]#, CorelationMap

if __name__=="__main__":
#    contrastMap, clusters, BG=main()
    ValOut=main()
    #Find the average value of all of the images and return it.
