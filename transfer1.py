# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:08:19 2016

@author: XuLiu
"""
import numpy
import datetime

transfer1=[]
for i in range(numpy.shape(start_station)[0]):
    for j in range(numpy.shape(terminal_station)[0]):
        if start_station[i]==terminal_station[j]:
            transfer1.append(start_station[i])
#以上得到所有可换乘的地铁站名    
traffic_line1=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer1)[0]):
            if data[m,1]==transfer1[k] and data[n,1]=='C' and data[m,0]==data[n,0]:
                runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                if runtime0.seconds<43200:
                    traffic_line1.append([data[m,0],runtime0,runtime0,'C',transfer1[k]])#第一次乘车的线名称
traffic_line1a=numpy.array(traffic_line1)
                    
traffic_line2=[]                    
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer1)[0]):
            if data[m,1]=='G' and data[n,1]==transfer1[k] and data[m,0]==data[n,0]:
                runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')#纯运行时间
                if runtime1.seconds<43200:
                    runtime1tot=runtime1+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))
                    traffic_line2.append([data[m,0],runtime1,runtime1tot,transfer1[k],'G'])#第二次乘车的线名称 
traffic_line2a=numpy.array(traffic_line2)
                    
    #求所有路径的耗时，与得到最优换乘路线：
totusetime=[]#所有可行路线的集合
mintot=traffic_line1a[0,2]+traffic_line2a[0,2]
for i in range(numpy.shape(traffic_line1a)[0]):
    for j in range(numpy.shape(traffic_line2a)[0]):
        if traffic_line1a[i,4]==traffic_line2a[j,3]:
            tot=traffic_line1a[i,2]+traffic_line2a[j,2]
            totusetime.append([tot.seconds/60,traffic_line1a[i,3],traffic_line1a[i,0],traffic_line1a[i,4],traffic_line2a[j,0],traffic_line2a[j,4]])
            if (mintot-tot).seconds<43200:
                transfer_bestline=[]
                transfer_beststation=[]
                mintot=tot
                transfer_beststation.append(traffic_line1a[i,4])
                transfer_bestline.append(traffic_line1a[i,0])
                transfer_bestline.append(traffic_line2a[j,0])
               
# 计算最优换乘路线下的末班车时间
timeend=[]
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(data)[0]):
        if transfer_bestline[1]==data[i,0]==data[j,0] and data[i,1]==transfer_beststation[0] and data[j,1]=='G':
            end1=datetime.datetime.strptime(data[i,2],'%H:%M')-datetime.timedelta(minutes=numpy.int(data[i,4]))-datetime.timedelta(minutes=numpy.int(data[i,5]))
            timeend.append(end1.strftime('%H:%M'))
            timeend.append(data[i,2])
###以上为正常计算末班车时间，第二个地铁线换乘站的末班时间-换乘时间-运行间隔-换乘之前的地铁运行时间
#出发站的末班车时间
trafficstation=[]
trafficstation.append('C')
trafficstation.append(transfer_beststation[0])
trafficstation.append('G')

for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[0] and data[i,1]=='C':
        start_endtime=[]
        start_endtime.append(data[i,2])
if timeend[0]<=start_endtime[0]:
    print(timeend,transfer_bestline,trafficstation,totusetime)
else:
    start_endtime.append(timeend[1])
    print(start_endtime,transfer_bestline,trafficstation,totusetime)
