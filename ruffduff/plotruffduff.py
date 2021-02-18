# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 18:24:12 2020

@author: sandra
"""

from geographiclib.geodesic import Geodesic
geod=Geodesic.WGS84
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def plot(latlonglist, r_wp,r, bearings, record):
    latlong = latlonglist
    i=0
    wp_ll=[]
    record_ll=[]
    while i<len(bearings):
        try:
            l_true = geod.Direct(latlong[0],latlong[1],bearings[i],r_wp)
            l_record= geod.Direct(latlong[0],latlong[1],int(record[i]),int(r[i]))
            wp_ll.append([l_true['lat2'],l_true['lon2']])
            record_ll.append([l_record['lat2'],l_record['lon2']])
            i+=1
        except:
            wp_ll.append([l_true['lat2'],l_true['lon2']])
            record_ll.append([np.nan,np.nan])
            i+=1
    
    return [wp_ll,record_ll]

def plotj(filename):
    readings=pd.read_csv(filename)
    profile_in_qn=readings['Profile'].unique()
    allfigs={'J1':[],'J2':[],'J3':[],'J4':[],'LINE_J':[],'LINE_NSRCC':[],'J1 WP10':[],'J2 WP1':[]}
    for p in profile_in_qn:
        sub=readings[readings['Profile']==p]
        freq_in_qn=sub['Frequency'].unique()
        for f in freq_in_qn:
            sub1=sub[sub['Frequency']==f]
            drone_in_qn=sub1['Drone'].unique()
            for u in drone_in_qn:
                sub2=sub1[sub1['Drone']==u]
                distance=np.array(sub2['Distance from Jammer'])
                ratio=np.array(sub2['Ratio'])
                xs=np.array([d*np.cos(45*np.pi/180) for d in distance])
                ys=np.array([d*np.cos(45*np.pi/180) for d in distance])
                zs=np.array(sub2['Height'])
                xt=np.linspace(0,1200,200)
                yt=xt
                plt.figure()
                ax=plt.gca(projection='3d')
                #print(xs,ys,zs)
                ax.scatter(xs,ys,zs)
                ax.plot(xt,yt,'r')
                ax.plot(0,0,'og')
                ax.set(xlabel='xDj (m)',ylabel='yDj (m)',zlabel='Height (m)')
                ax.set_xlim([0,1200])
                ax.set_xticks(np.linspace(0,1200,4))
                ax.set_ylim([0,1200])
                ax.set_yticks(np.linspace(0,1200,4))
                idx=0
                while idx < len(zs):
                    anno='Hgt: %i, Range: %i, DjDv: %0.2f' %(zs[idx],distance[idx],ratio[idx])
                    ax.text(xs[idx],ys[idx],zs[idx],anno)
                    idx+=1
                ax.set_title('%s, %s, %sGHz' %(u,p,str(f)))
                ax.view_init(7,230)
                figname='%s_%s_%sGHz.png' %(u,p,str(f))
                plt.savefig(figname,dpi=300)
                allfigs[p].append(figname)
                plt.close()
    allfigs=pd.DataFrame.from_dict(allfigs,orient='index')
    return allfigs