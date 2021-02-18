# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 12:17:46 2020

@author: sandra
"""

import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service(r'C:\Users\this_\Downloads\chromedriver_85.exe')
service.start()
from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84
from plotruffduff import plot
import pandas as pd
import numpy as np

#initialise sandbox details
latlong = [1.327626, 103.982114]   #rfdf latlong
frame=pd.read_csv('BST_template.csv')
m = folium.Map(location=[latlong[0],latlong[1]],zoom_start=16,tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite
#---------------------------------------------------------------------------------------------------

#file should contain SBname, height, r, bearing, record

#initialise sb details
SB3={'name':'SB3','bearings':[203,188,173,158,143,128,113,98,83,68,53,38,23],'wps':13,'r':1000}
SB4={'name':'SB4','bearings':[203,218,233,248,263,278,293,308,323,338,353,8],'wps':12,'r':1000}
sandboxes=[SB3,SB4]

#filter out each sandbox
sandbox_in_qn=[]
i=0
while i<len(sandboxes):
    sandbox_in_qn.append(frame[frame['SBname']==sandboxes[i]['name']])
    i+=1
    
#drone > freq > height
#partitions1= P4 2.4 <=100, P4 2.4 125, P4 5.8 <=100, P4 5.8 125
#partitions3= Mavic 1, Mavic 2 2.4 <=100, Mavic 2 2.4 125

toprocess=frame #loop
partitions1_1=toprocess[(toprocess['Height']<=100)&(toprocess['Drone']=='P4')&(toprocess['Freq']==2.4)]
partitions1_2=toprocess[(toprocess['Height']==125)&(toprocess['Drone']=='P4')&(toprocess['Freq']==2.4)]
partitions1_3=toprocess[(toprocess['Height']<=100)&(toprocess['Drone']=='P4')&(toprocess['Freq']==5.8)]
partitions1_4=toprocess[(toprocess['Height']==125)&(toprocess['Drone']=='P4')&(toprocess['Freq']==5.8)]
partitions2_1=toprocess[(toprocess['Drone']=='Mavic 1')]
partitions2_2=toprocess[(toprocess['Height']<=100)&(toprocess['Drone']=='Mavic 2')]
partitions2_3=toprocess[(toprocess['Height']==125)&(toprocess['Drone']=='Mavic 2')]

partitions=[partitions1_1,partitions1_2,partitions1_3,partitions1_4,partitions2_1,partitions2_2,partitions2_3]

#seems like you need to run this one by one
k=partitions2_3
#for k in partitions:
SBname=k['SBname'].unique()
#further partition into SBs
for d in SBname:
    SB_part=k[k['SBname']==d]
    drone=SB_part['Drone'].iloc[0]
    if SB_part['Height'].iloc[0]<=100:
        height= 'equalorlessthan100'
    elif SB_part['Height'].iloc[0]>=250:
        height='250-300'
    else:
        height='125'
    r=np.array(SB_part['Recorded Range'])
    for sb in sandboxes:
        if sb['name']==SB_part['SBname'].iloc[0]:
            r_wp=sb['r']
    record=np.array(SB_part['Record'])
    freq=SB_part['Freq'].iloc[0]
    for sb in sandboxes:
        if sb['name']==SB_part['SBname'].iloc[0]:
            bearings=sb['bearings']
    
    #---------------------------------------------------------------------------------------------------
    #mapping block
        
    #initialise map

    folium.Marker(location=[latlong[0],latlong[1]]).add_to(m)
    folium.Circle(radius=500,location=[latlong[0],latlong[1]],color='purple',fill=False).add_to(m)
    folium.Circle(radius=1000,location=[latlong[0],latlong[1]],color='yellow',fill=False).add_to(m)
    
    #loop here to plot maps
    output=plot(latlong,r_wp,r,bearings,record)   #my own function go here to loop
    
    wp_ll=output[0]
    record_ll=output[1]
    rms=[]
    
    j=0
    while j<len(wp_ll):
        [latitude,longitude]=wp_ll[j]
        [latitude1,longitude1]=record_ll[j]
        try:
            rms.append(float(record[j])-float(bearings[j]))
            wpname='%s\n WP %i\nError: %d\u00b0' %(SB_part['SBname'].iloc[0],j+1,float(record[j])-float(bearings[j]))
            folium.Circle([latitude,longitude],popup=folium.Popup(wpname,max_width=78,show=True,sticky=True),radius=20,color='black',fill_color='violet',fill_opacity=1).add_to(m)
            folium.Circle([latitude1,longitude1],radius=20,color=False,fill_color='blue',fill_opacity=1).add_to(m)
            folium.PolyLine((wp_ll[j],record_ll[j]),color='red').add_to(m)
            j+=1
        except:
            measured=[0]
            for measure in measured:
                if j+1==measure:
                    wpname='%s\n No detection at WP %i\n' %(SB_part['SBname'].iloc[0],j+1)
                    folium.Circle([latitude,longitude],popup=folium.Popup(wpname,max_width=78,show=True,sticky=True),radius=20,color='red',fill_color='False',fill_opacity=1).add_to(m)
                    folium.PolyLine((wp_ll[j],(latlong[0],latlong[1])),color='red').add_to(m)
                elif j+1==1:
                    pass
                else:
                    #wpname='%s\n No measurement taken at WP %i\n' %(SB_part['SBname'].iloc[0],j+1)
                    folium.Circle([latitude,longitude],radius=20,color='black',fill_color='violet',fill_opacity=1).add_to(m)
            j+=1

#calculate rms
rms_val=np.sqrt(np.mean(np.array(rms)**2))

#final map stuff - to include in the loop too
#cool thing to plot a legend
legend_html =   '''
                <div style="background: #C8C8C8;
                            position: fixed; 
                            bottom: 50px; left: 30px; width: 370px; height: 223px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            "
                            >
                            &nbsp; <b><u>Legend</u><b></br>
                            <br>&nbsp; Test: %s, %sm height, %0.1fGHz &nbsp;<br>
                            <br>&nbsp; RFDF &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
                            <br>&nbsp; 500m &nbsp; <i class="fa fa-circle-o" style="color:purple"></i><br>
                            <br>&nbsp; 1000m &nbsp; <i class="fa fa-circle-o" style="color:yellow"></i><br>
                </div>
                ''' %(drone,height,freq)
    
m.get_root().html.add_child(folium.Element(legend_html))

mapname='%s_%smheight_%0.1fGHz.html' %(drone,height,freq)
m.save(mapname) #INTERACTIVE MAP
driver = webdriver.Remote(service.service_url)
openthis=r'C:\Users\this_\Documents\Python Scripts\testingfolium\ruffduff\%s' %(mapname)
driver.get(openthis)
pic_name='%s_%smheight_%0.1fGHz.png' %(drone,height,freq)
driver.save_screenshot(pic_name)
driver.quit()
print('Screenshot of map taken.')