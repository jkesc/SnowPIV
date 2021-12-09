# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""
#To do:
#It seems like some parts get larger values at false locations. probably because the range is fuzzy(not 1 or 0). Should make it either snowflake or noflake, in order to avoid this.
#Should also confine it to one size of snowflakes. At it is now. one flake close to thecamera always results in large values, so all vectors point towards it.
#Also: maybe find a way to reduce the resoultion of the picture to get fewer pixels -> fewer iterations?
#main function
#import cv2
import FilterBG as FBG
import GetContrast as GC
import FindCluster as FC
import CrossCorelation as CC
import Visualization as VS

def flakeRange(Map,lower,upper):
    cluster=FC.getClusters(Map)
    out=FC.colorCluster(cluster,Map,lower,upper,255,0)
    return out[0]

def main():
    import cv2
#    frame1=cv2.imread("testPic1.png")
#    frame2=cv2.imread("testPic2.png")
#    result = cv2.matchTemplate(frame1,frame1[10:100,20:100],cv2.TM_CCOEFF)
#    return [frame1, frame2,result]
    videoname='testPiv.mp4'#'PIV2.mp4'#
    BG=FBG.GetBG(videoname)
    treshold=1#contrast threshold
    minFlakeSize=1
    maxFlakeSize=10000
    vid = cv2.VideoCapture("PIV2.mp4")
    frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(frames-1):
        contrastMap0=GC.RemoveBG(BG,videoname,record=False,ContrastTreshold=treshold,filename=str(treshold)+'.avi',frame=i)
        contrastMap1=GC.RemoveBG(BG,videoname,record=False,ContrastTreshold=treshold,filename=str(treshold)+'.avi',frame=i+1)
        print('read maps for iteration '+str(i)+'\n')
        contrastMap0=flakeRange(contrastMap0,minFlakeSize,maxFlakeSize)#[0:600,250:1000][0:400,250:650]
        contrastMap1=flakeRange(contrastMap1,minFlakeSize,maxFlakeSize)
        print('Filtered flakes for iteration '+str(i)+'\n')
        dx,dy,idx=CC.crossCorelateFramesCV2(contrastMap0,10,contrastMap1,True)
        image=VS.vectorField(contrastMap0,dx,dy,idx)
        image.savefig('vectorField_frame_'+str(i)+'flakeRange'+str(minFlakeSize)+','+str(maxFlakeSize)+'.png')
        image.clf()
    return [contrastMap0,contrastMap1,BG,dx,dy,idx]#, corelationmap

if __name__=="__main__":
#    contrastMap, clusters, BG=main()
    ValOut=main()