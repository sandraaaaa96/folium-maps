# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:07:56 2020

@author: sandra
"""


import folium
import re
import pandas as pd
#import math
import numpy as np
from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84
import webbrowser
from processing_logs import processing_logs as pl

#CHANGE THIS AND ALL WILL PROCEED
file_name='dat_6'
#--------------------------------------------------------------------------------------------------------------
#process logs
#print(pl(file_name))
#---------------------------------------------------------------------------------------------------------------
#find instance of radar and its latlong from initialising block

# pat=re.compile('received radar with',re.IGNORECASE) #find instancing of radar
# lines=[]
# i=0
# with open(file_name,'rt') as myfile:
#     for line in myfile:
#         i+=1
#         if pat.search(line) !=None:
#             lines.append((i,line.rstrip('\n')))
            
# first_instance='Line ' + str(lines[0][0])+ ': ' + lines[0][1]

# #extract latlong
# pat_latlongalt='\d{1,3}[.]\d{5,10}'
# latlongalt=re.findall(pat_latlongalt,first_instance)
latlongalt=[1.340847,103.975315]  #changi airport R radar

#--------------------------------------------------------------------------------------------------------------
#MAP BLOCK and radar track processing

m = folium.Map(location=[latlongalt[0],latlongalt[1]],zoom_start=15,
                tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite

folium.Marker(location=[latlongalt[0],latlongalt[1]],popup='Radar').add_to(m)
#range rings
folium.Circle(radius=1000,location=[latlongalt[0],latlongalt[1]],color='yellow',fill=False).add_to(m)
folium.Circle(radius=2000,location=[latlongalt[0],latlongalt[1]],color='yellow',fill=False).add_to(m)
folium.Circle(radius=3000,location=[latlongalt[0],latlongalt[1]],color='yellow',fill=False).add_to(m)
folium.Circle(radius=4000,location=[latlongalt[0],latlongalt[1]],color='yellow',fill=False).add_to(m)
folium.Circle(radius=5000,location=[latlongalt[0],latlongalt[1]],color='yellow',fill=False).add_to(m)
# folium.Marker(location=[latlongalt_cam[0],latlongalt_cam[1]],popup='EOS').add_to(m)

#open radar detections csv
radardetectionfile='radardetectioninfo_%s.csv' %(file_name)   #link created csv from here
frame = pd.read_csv(radardetectionfile)
latlong_radar=[float(latlongalt[0]),float(latlongalt[1])]

#filter out azelr
azelr=frame.filter(items=['Azimuth','Z','Range'])
data_track=np.array(azelr)

tracklatlong=[]

for az,el,r in data_track:
    l = geod.Direct(latlong_radar[0],latlong_radar[1],az,r)   #THIS IS TOO GOOD
    height=el
    tracklatlong.append([l['lat2'],l['lon2'],height])

tracklatlong=np.array(tracklatlong)

for latitude,longitude,height in tracklatlong:
    folium.Circle([latitude,longitude],popup=str(height),radius=0.3,color='red',fill_color=False,fill_opacity=0.5).add_to(m)
    
#m #display map in jupyter

mapname='track_%s.html' %(file_name)
m.save(mapname) #INTERACTIVE MAP
webbrowser.open_new_tab(mapname) #open in default browser
print("Logs plotted, exited with 0 errors.")
