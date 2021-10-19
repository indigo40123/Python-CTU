# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 23:29:08 2021

@author: Feng
"""
from urllib.request import urlopen
import json
import time
import pandas as pd 
import os


def data_transform(timestamp,latitude,longitude):
     human_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(timestamp))
     #print(human_time)
     
     la = latitude.split(".")
     la_degree= int(float(la[0]))
     la_minutes = int(float(la[1])/10000*60)
     la_rest = float(la[1])/10000*60-int(float(la[1])/10000*60)
     la_second = int(la_rest*60)
     new_la = str(la_degree)+"°"+str(la_minutes)+"'"+str(la_second)+'"'
     #print(new_la)

     lo = longitude.split(".")
     lo_degree= int(float(lo[0]))
     lo_minutes = int(float(lo[1])/10000*60)
     lo_rest = float(lo[1])/10000*60-int(float(lo[1])/10000*60)
     lo_second = int(lo_rest*60)
     new_lo = str(lo_degree)+"°"+str(lo_minutes)+"'"+str(lo_second)+'"'
     #print(new_lo)
     
     return(human_time,new_la,new_lo)
 
def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec
 
    
second = sleep_time(0, 0, 5)
ticks = time.time()
ticks_end = ticks+120

while True:
    if time.time()< ticks_end:
        filepath = "HW4.csv"
        if os.path.isfile(filepath):
            req = ("http://api.open-notify.org/iss-now.json")
            response = urlopen(req)
            obj = json.loads(response.read())
            data_transform(obj['timestamp'],obj['iss_position']['latitude'],obj['iss_position']['longitude'])
            result = data_transform(obj['timestamp'],obj['iss_position']['latitude'],obj['iss_position']['longitude'])
        
            df1 = pd.read_csv("HW4.csv")
            df2 = pd.DataFrame({"timestamp":[obj['timestamp']], 
                                "human_time":[result[0]],
                                "latitude":[result[1]],
                                "longitude":[result[2]],}) 
            df1 = df1.append(df2,ignore_index=True)
            df1.to_csv("HW4.csv",index=False)
            time.sleep(second)
        else: 
            df1 = pd.DataFrame({"timestamp": [], 
                                "human_time":[],
                                "latitude":[],
                                "longitude":[]})
            df1.to_csv("HW4.csv",index=False)
    else: break





