# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:41:00 2020

@author: sandra
"""

import json
import pandas as pd

#workflow: write all the track info from detections file

detections=open('track_detections.json','r')
detections_csv=open('detections_bst.csv','w+')
detections_csv.write('TrackID,Acquired Time (UTC),Last Updated (UTC),Duration (s),Range (m),Lat,Long,Altitude (m),velMag (m/s),Stats-rcs,Stats-sv3,Stats-sva,Stats-vmg,probUAS,probUnknown,class-clutter,class-organic,class-inorganic\n')
#iterate over all lines
line_detections=detections.readlines()
i=0
while i < len(line_detections):
    line=line_detections[i]
    layer1=json.loads(line)
    metrics=layer1['metrics']   #metrics for classification
    trackinfo=layer1['xtra']['track']     #trackinfo
    
    #info
    trackid=trackinfo['name']
    acquiredtime=pd.to_datetime(trackinfo['acquiredTime'],unit='ms',utc=True)
    lastupdated=pd.to_datetime(trackinfo['lastUpdateTime'],unit='ms',utc=True)
    duration=trackinfo['observation']['duration']
    track_range=trackinfo['observation']['range']
    lat=trackinfo['geolocation']['latitude']
    long=trackinfo['geolocation']['longitude']
    altitude=trackinfo['geolocation']['altitude']
    velmag=trackinfo['geolocation']['velMag']
    rcs=metrics['stats']['rcs']
    sv3=metrics['stats']['sv3']
    sva=metrics['stats']['sva']
    vmg=metrics['stats']['vmg']
    probUAS=trackinfo['stats']['probUAS']
    probUnknown=trackinfo['stats']['probUnknown']
    clutter=metrics['classifications']['clutter']
    organic=metrics['classifications']['organic']
    inorganic=metrics['classifications']['inorganic']
    
    string='%s,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i,%i,%f,%f,%f\n' %(trackid,acquiredtime,lastupdated,duration,track_range,lat,long,altitude,velmag,rcs,sv3,sva,vmg,probUAS,probUnknown,clutter,organic,inorganic)
    
    detections_csv.write(string)
    print(trackid)
    i+=1

detections_csv.close()
detections.close()