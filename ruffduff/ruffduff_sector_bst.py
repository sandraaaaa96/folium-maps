# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:51:13 2020

@author: sandra
"""

import folium
from folium import plugins
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service(r'C:\Users\this_\Downloads\chromedriver_85.exe')
service.start()
from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84
from plotruffduff import plotj
import skimage.io
from skimage.transform import resize
from skimage.util import img_as_ubyte

latlong = [1.327626, 103.982114]   #jammer latlong

#initialise jamming profiles
profiles={'LINE_J':{'launch':[1.336552, 103.989351],'direction':40,'arc':38},\
          'LINE_NSRCC':{'launch':[1.321433, 103.973577],'direction':235,'arc':38}}
    
m = folium.Map(location=[latlong[0],latlong[1]],zoom_start=15,tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite

#plot all profiles
for key in profiles:

    line_az=geod.Inverse(latlong[0],latlong[1],profiles[key]['launch'][0],profiles[key]['launch'][1])['azi1']
    profiles[key]['azi']=line_az
    WP1=[geod.Direct(latlong[0],latlong[1],line_az,1000)['lat2'],geod.Direct(latlong[0],latlong[1],line_az,1000)['lon2']]
    
    #initialise map with flight path and jammer coverage
    folium.Marker(location=latlong).add_to(m)
    folium.Marker(location=profiles[key]['launch']).add_to(m)
    folium.Marker(location=WP1).add_to(m)
    folium.PolyLine((latlong,profiles[key]['launch']),color='blue').add_to(m)
    
    #jammer coverage
    plugins.semicircle.SemiCircle(
        location=latlong,   # Location of center
        radius= 1000,               # Radius in meters
        direction= profiles[key]['direction'],             # Direction of cone center (0 to 360 degrees)
        arc=profiles[key]['arc'],                     # Amplitude of cone (0 to 360 degrees)
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.3
    ).add_to(m)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#record readings
#readings consist of profile name, drone type, frequency, distance flown in, height
allfigs=plotj('BSTJ.csv')
allfigs.iloc[5,3]=allfigs.iloc[5,1]
allfigs.iloc[5,1]=None

#plot graphs on map
no_maps=allfigs.shape[1]

#generate 1 by 1 from 0 to 4/5
idm=3
bottom_left={'J1':[40,75],'J2':[70,40],'J3':[10,30],'J4':[40,0],'LINE_J':[50,67],'LINE_NSRCC':[30,3]}
map_no=idm+1
paths=allfigs.iloc[:,idm]
for path in paths:
    try:
        image=skimage.io.imread(path)
        image=resize(image,(image.shape[0]//5,image.shape[1]//5),anti_aliasing=True)
        image=img_as_ubyte(image)
        skimage.io.imsave(path,image)
        #FloatImage
        plugins.float_image.FloatImage(path, bottom=bottom_left[paths[paths==path].index[0]][0], left=bottom_left[paths[paths==path].index[0]][1]).add_to(m)
    except:
        pass
idm+=1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#mapping block
mapname='sector%i.html' %(map_no)
m.save(mapname) #INTERACTIVE MAP