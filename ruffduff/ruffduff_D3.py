# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:46:57 2020

@author: sandra
"""

import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service = Service(r'C:\Users\this_\Downloads\chromedriver_86.exe')
service.start()
from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84
from plotruffduff import plot
import pandas as pd
import numpy as np

#initialise sandbox details
latlong = [1.3461667,103.9772245]   #rfdf latlong
frame=pd.read_csv('DSO_template.csv')
m = folium.Map(location=[latlong[0],latlong[1]],zoom_start=16,tiles='http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Coded and Produced by Sandra Ng Yi Ling, DSTA 2020 \u00a9') #google satellite
#---------------------------------------------------------------------------------------------------

#file should contain SBname, height, r, bearing, record

#initialise sb details
SB2={'name':'Sandbox 2','bearings':[203,218,233,248,263,278],'wps':6,'r':1000}
SB3={'name':'Sandbox 3','bearings':[8, 353, 338, 323, 308, 293],'wps':6,'r':1000}
SB8={'name':'Sandbox 8','bearings':[203, 188, 173, 158, 153, 143],'wps':6,'r':500}
SB9={'name':'Sandbox 9','bearings':[203, 188, 173, 158, 143, 128, 113],'wps':7,'r':1000}
SB9_LP={'name':'Sandbox 9 LP','bearings':[159],'wps':1,'r':780}
sandboxes=[SB2,SB3,SB8,SB9,SB9_LP]

#filter out each sandbox
sandbox_in_qn=[]
i=0
while i<len(sandboxes):
    sandbox_in_qn.append(frame[frame['SBname']==sandboxes[i]['name']])
    i+=1
    
#drone > freq > height > band
#partitions1= P4PV1 5.8 100m, 200m, 300m
#partitions2= P4PV2 2.4 100m, 200m, 300m
#partitions3= Mavic 2.4 100m, 200m, 300m
#partition4= 3DR 433 3 bands 100m, 200m, 300m
#partition5= 3DR 433 1 band 100m, 200m, 300m
#partition6= RFD900 915 100m, 200m, 300m
toprocess=frame #loop
partitions1_1=toprocess[(toprocess['Height']==100)&(toprocess['Drone']=='P4PV1')]
partitions1_2=toprocess[(toprocess['Height']==200)&(toprocess['Drone']=='P4PV1')]
partitions1_3=toprocess[(toprocess['Height']==300)&(toprocess['Drone']=='P4PV1')]
partitions2_1=toprocess[(toprocess['Height']==100)&(toprocess['Drone']=='P4PV2')]
partitions2_2=toprocess[(toprocess['Height']==200)&(toprocess['Drone']=='P4PV2')]
partitions2_3=toprocess[(toprocess['Height']==300)&(toprocess['Drone']=='P4PV2')]
partitions3_1=toprocess[(toprocess['Height']==100)&(toprocess['Drone']=='Mavic 2')]
partitions3_2=toprocess[(toprocess['Height']==200)&(toprocess['Drone']=='Mavic 2')]
partitions3_3=toprocess[(toprocess['Height']==300)&(toprocess['Drone']=='Mavic 2')]
partitions4_1=toprocess[(toprocess['Height']==100)&(toprocess['Drone']=='3DR')&(toprocess['Band']==3)]
partitions4_2=toprocess[(toprocess['Height']==200)&(toprocess['Drone']=='3DR')&(toprocess['Band']==3)]
partitions4_3=toprocess[(toprocess['Height']==300)&(toprocess['Drone']=='3DR')&(toprocess['Band']==3)]
partitions5_1=toprocess[(toprocess['Height']==100)&(toprocess['Band']==1)&(toprocess['Drone']=='3DR')]
partitions5_2=toprocess[(toprocess['Height']==200)&(toprocess['Band']==1)&(toprocess['Drone']=='3DR')]
partitions5_3=toprocess[(toprocess['Height']==300)&(toprocess['Band']==1)&(toprocess['Drone']=='3DR')]
partitions6_1=toprocess[(toprocess['Height']==100)&(toprocess['Drone']=='RFD900')]
partitions6_2=toprocess[(toprocess['Height']==200)&(toprocess['Drone']=='RFD900')]
partitions6_3=toprocess[(toprocess['Height']==300)&(toprocess['Drone']=='RFD900')]

partitions=[partitions1_1,partitions1_2,partitions1_3,partitions2_1,partitions2_2,partitions2_3,partitions3_1,partitions3_2,partitions3_3,partitions4_1,partitions4_2,partitions4_3,partitions5_1,partitions5_2,partitions5_3,partitions6_1,partitions6_2,partitions6_3]

#seems like you need to run this one by one
k=partitions6_3
#for k in partitions:
SBname=k['SBname'].unique()
#further partition into SBs
for d in SBname:
    SB_part=k[k['SBname']==d]
    drone=SB_part['Drone'].iloc[0]
    if SB_part['Height'].iloc[0]<=100:
        height= '100'
    elif SB_part['Height'].iloc[0]>=250:
        height='300'
    else:
        height='150-200'
    r=np.array(SB_part['Recorded Range'])
    for sb in sandboxes:
        if sb['name']==SB_part['SBname'].iloc[0]:
            r_wp=sb['r']
    record=np.array(SB_part['Record'])
    freq=SB_part['Freq'].iloc[0]
    for sb in sandboxes:
        if sb['name']==SB_part['SBname'].iloc[0]:
            bearings=sb['bearings']
    band=SB_part['Band'].iloc[0]
    
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
            #wpname='%s\n Not tested at WP %i\n' %(SB_part['SBname'].iloc[0],j+1)
            wpname='Not tested\n'
            folium.Circle([latitude,longitude],popup=folium.Popup(wpname,max_width=78,show=True,sticky=True),radius=20,color='red',fill_color='False',fill_opacity=1).add_to(m)
            #folium.PolyLine((wp_ll[j],(latlong[0],latlong[1])),color='red').add_to(m)
            j+=1

#calculate rms
#rms_val=np.sqrt(np.mean(np.array(rms)**2))

#final map stuff - to include in the loop too
#cool thing to plot a legend
legend_html =   '''
                <div style="background: #C8C8C8;
                            position: fixed; 
                            bottom: 50px; left: 30px; width: 360px; height: 223px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            "
                            >
                            &nbsp; <b><u>Legend</u><b></br>
                            <br>&nbsp; Test: %s, %sm height, %0.1fGHz on %i band(s) &nbsp;<br>
                            <br>&nbsp; RFDF &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
                            <br>&nbsp; 500m &nbsp; <i class="fa fa-circle-o" style="color:purple"></i><br>
                            <br>&nbsp; 1000m &nbsp; <i class="fa fa-circle-o" style="color:yellow"></i><br>
                </div>
                ''' %(drone,height,freq,band)
    
m.get_root().html.add_child(folium.Element(legend_html))

mapname='%s_%smheight_%0.1fGHz_%i.html' %(drone,height,freq,band)
m.save(mapname) #INTERACTIVE MAP
driver = webdriver.Remote(service.service_url)
openthis=r'C:\Users\this_\Documents\Python Scripts\testingfolium\ruffduff\%s' %(mapname)
driver.get(openthis)
#pic_name='%s_%smheight_%0.1fGHz_%i.png' %(drone,height,freq,band)
#driver.save_screenshot(pic_name)
#driver.quit()
print('Screenshot of map taken.')
    