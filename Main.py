# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:53:47 2021

@author: jkescher
"""

#main function
import FilterBG as FBG
import GetContrast as GC
import FindCluster as FC

BG=FBG.GetBG('PIV2.mp4')
i=100
contrastMap=GC.RemoveBG(BG,'PIV2.mp4',False,i,str(i)+'.avi')
clusters=FC.getClusters(contrastMap)