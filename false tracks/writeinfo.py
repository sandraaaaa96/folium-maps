# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:25:43 2020

@author: sandra
"""
import re
import math
import numpy as np

def writeinfo(all_lines,cycles,index):
    cyclename=cycles[index][0]
    startline=cycles[index][1]
    endline=cycles[index][2]
    
    cyclelines=[]
    for n in range(startline,endline+1,1):
        n+=1
        line_to_add=all_lines[n][1]
        cyclelines.append(line_to_add)
    
    radardetectionlines=[]
    eodetectionlines=[]
    pat_radard=re.compile('pDataReception : plotId') #take the last line after Wahba correction
    pat_eod=re.compile('sensorType = 8')   
    
    for line in cyclelines:
        if pat_radard.search(line) !=None:
            radardetectionlines.append(line.rstrip('\n'))
        elif pat_eod.search(line) !=None:
            eodetectionlines.append(line.rstrip('\n'))
        else:
            continue
    
    #---------------------------------------------------------------------------------------------------------------
    #from radardetectionlines filter out the plotAz, plotEl, plotRange, plotAzVar, plotElVar, plotRangeVar
    #search_terms=['plotAz', 'plotEl', 'plotRange', 'plotAzVar', 'plotElVar', 'plotRangeVar']
            
    all_radar_info=[]
    
    for line in radardetectionlines:
        data=line.split(',')
        datetime=re.findall('\d{4}[-]\d{2}[-]\d{2}[\s]\d{2}[:]\d{2}[:]\d{2}',data[0])[0]
        trackID=re.findall('\d{3,6}',data[1])[2]
        X=float(re.findall('[\s-]\d+',data[2])[0])
        Y=float(re.findall('[\s-]\d+',data[3])[0])
        Z=float(data[8])-float(data[5])
        Range=math.sqrt(math.pow(X,2)+math.pow(Y,2))
        Az=(math.atan(abs(Y)/abs(X)))*180/math.pi
        #plot offset to correct for circle
        if (np.sign(X)==-1) and (np.sign(Y)==1):
            Az=float(180-Az)
        elif (np.sign(X)==-1) and (np.sign(Y)==-1):
            Az=float(180+Az)
        elif (np.sign(X)==1) and (np.sign(Y)==-1):
            Az=float(360-Az)
        else:
            Az=float(Az)
        
        info_str="%s,%s,%s,%f,%f,%f,%f,%f\n" %(datetime,cyclename,trackID,X,Y,Z,Range,Az)
        all_radar_info.append(info_str)
        
    #-----------------------------------------------------------------------------------------------------------------
    #do the same for EO
    all_eo_info=[]
    
    for line in eodetectionlines:
        data_eo=line.split(',')
        datetime=re.findall('\d{4}[-]\d{2}[-]\d{2}[\s]\d{2}[:]\d{2}[:]\d{2}',data[0])[0]
        trackID=re.findall('\d+',data_eo[3])[0]
        plotAz=re.findall('[\s-]\w[.]\d+',data_eo[6])[0]
        plotEl=re.findall('[\s-]\w[.]\d+',data_eo[8])[0]
        plotRange=re.findall('\d+[.]\d+',data_eo[9])[0]
        plotAzVar=re.findall('\d+[.]\d+',data_eo[11])[0]
        plotElVar=re.findall('\d+[.]\d+',data_eo[12])[0]
        plotRangeVar=re.findall('\d+[.]\d+',data_eo[13])[0]
        
    #cyclenumber  #trackid=3  #plotAz=5,6   #plotEl=7,8  #plotRange=9 #plotAzVar=11  #plotElVar=12  #plotRangeVar=13
        
        eo_info_str="%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %(datetime,cyclename,trackID,plotAz,plotEl,plotRange,plotAzVar,plotElVar,plotRangeVar)
        all_eo_info.append(eo_info_str)
    
    return [all_radar_info,all_eo_info]