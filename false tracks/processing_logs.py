# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:38:46 2020

@author: sandra
"""
import re
import sys
from writeinfo import writeinfo

def processing_logs(filename):

    #all lines
    all_lines=[]
    file_name_full=filename
    all=0
    with open(file_name_full,'rt') as myfile:
        for line in myfile:
            all+=1
            all_lines.append((all,line.rstrip('\n')))
    
    #--------------------------------------------------------------------------------------------------------------
    #extract SA tracks in the form of spherical coordinates from cycle block
    
    pat_cyclestart=re.compile('Cycle started') #find instancing of recording cycle
    pat_cycleend=re.compile('Cycle Finished') #find ending of recording cycle
    
    lines_start=[]
    lines_end=[]
    i=0
    file_name_cycle=file_name_full
    with open(file_name_cycle,'rt') as myfile:
        for line in myfile:
            i+=1
            if pat_cyclestart.search(line) !=None:
                lines_start.append((i,line.rstrip('\n')))
            elif pat_cycleend.search(line) !=None:
                lines_end.append((i,line.rstrip('\n')))
            else:
                continue
    
    j=0
    cycles=[]
    #group range of line indexes to bound search per cycle #need to minus 1
    while j<min(len(lines_start),len(lines_end)): #to remove any errors of not matched(?) even though why is it mismatched
        cyclename='Cycle %i'%(j+1)
        start_index=lines_start[j][0]
        end_index=lines_end[j][0]
        cycles.append([cyclename,start_index,end_index])
        j=j+1
        
    #---------------------------------------------------------------------------------------------------------------
    #create the csv first
    csvname='radardetectioninfo_%s.csv' %(filename)
    csvname_eo='eodetectioninfo_%s.csv' %(filename)
    csvfile=open(csvname, "w+")
    csvfile_eo=open(csvname_eo,"w+")
    csvheader_radar='Datetime, Cycle,TrackID,X,Y,Z,Range,Azimuth\n'
    csvheader='Datetime, Cycle,TrackID,plotAz,plotEl,plotRange,plotAzVar,plotElVar,plotRangeVar\n'
    csvfile.write(csvheader_radar)
    csvfile_eo.write(csvheader)
    error=[]
    
    index=0
    while index<len(cycles):
        #print(index) #for debug
        try:
            output=writeinfo(all_lines,cycles,index)
            for string in output[0]:
                csvfile.write(string)
            for string1 in output[1]:
                csvfile_eo.write(string1)
            index+=1
        except:
            error.append((index,str(sys.exc_info()[0])))
            #handle the error, dont want to handle it now
            index+=1
    errors=len(error)*100/len(cycles)
    csvfile.close()
    csvfile_eo.close()
    error_line="Logs processed, exited with %0.2f percent error." %(errors)
    return(error_line)  #exited with no errors

