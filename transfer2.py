# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:44:26 2016

@author: XuLiu
"""

def startline_station(data,ss,ls):#看经过起点的地铁线经过的地铁站，经过这些地铁站还有哪些线,然后这些线经过的点,即看出发点换乘一次可以达到的所有的地铁站                
    lts=[]
    for i in range(unique(numpy.shape(ss))[0]):
        for j in range(numpy.shape(data)[0]):
            if ss[i]==data[j,1] and data[j,0] not in ls:
                lts.append(data[j,0])
    ltss=[]#看上一条线还过哪些点
    for i in range(unique(numpy.shape(lts))[0]):
        for j in range(numpy.shape(data)[0]):
            if lts[i]==data[j,0] and data[j,1] not in ss:
                ltss.append(data[j,1])
    return(unique(lts),unique(ltss))




transfertwo_line,transfertwo_station=startline_station(data,start_station,lines)

transfertwos=[]#第二次换乘的车站
for i in range(numpy.shape(terminal_station)[0]):
    for j in range(numpy.shape(transfertwo_station)[0]):
        if terminal_station[i]==transfertwo_station[j]:
            transfertwos.append(transfertwo_station[j])
transfertwostation=unique(transfertwos)

transfertwol=[]#第二次乘坐的线           
for m in transfertwostation:
    for n in start_station:
        for i in range(numpy.shape(data)[0]):
            for j in range(numpy.shape(data)[0]):
                if data[i,1]==m and data[j,1]==n and data[i,0]==data[j,0]:
                    transfertwol.append(data[i,0])
transfertwoline=unique(transfertwol)
            
#if  poss_transfers_two!=[]:
    #return('T') 
            
#其中runtimetot都包括此段的运行时间与上一段到此段的步行时间与运行间隔
traffic_line1=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(start_station)[0]):
            if data[m,1]==start_station[k] and data[n,1]=='F' and data[m,0]==data[n,0]:
                runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                if runtime0.seconds<43200:
                    traffic_line1.append([data[m,0],runtime0,runtime0,'F',start_station[k]])#第一次乘车的线名称
traffic_line1a=numpy.array(traffic_line1)

traffic_line2=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfertwostation)[0]):
            for l in range(numpy.shape(traffic_line1a)[0]):
                if data[m,1]==transfertwostation[k] and data[n,1]==traffic_line1a[l,4] and data[m,0]==data[n,0]:
                    runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime1.seconds<43200:
                        runtime1tot=runtime1+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                        traffic_line2.append([data[m,0],runtime1,runtime1tot,traffic_line1a[l,4],transfertwostation[k]])#第二次乘车的线名称
traffic_line2a=numpy.array(traffic_line2)


traffic_line3=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfertwostation)[0]):
            if data[m,1]=='E' and data[n,1]==transfertwostation[k] and data[m,0]==data[n,0]:
                runtime2=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                if runtime2.seconds<43200:
                    runtime2tot=runtime2+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                    traffic_line3.append([data[m,0],runtime2,runtime2tot,transfertwostation[k],'E'])#第三次乘车的线名称
traffic_line3a=numpy.array(traffic_line3)

                  
    #求所有路径的耗时，与得到最优换乘路线：
totusetime=[]

mintot=datetime.timedelta(0,43200)
for i in range(numpy.shape(traffic_line1a)[0]):
    for j in range(numpy.shape(traffic_line2a)[0]):
        for k in range(numpy.shape(traffic_line3a)[0]):
            if traffic_line1a[i,4]==traffic_line2a[j,3]:
                if traffic_line2a[j,4]==traffic_line3a[k,3]:
                    tot=traffic_line1a[i,2]+traffic_line2a[j,2]+traffic_line3a[k,2]
                    totusetime.append([(tot.seconds/60),traffic_line1a[i,3],traffic_line1a[i,0],traffic_line2a[j,3],traffic_line2a[j,0],traffic_line3a[k,3],traffic_line3a[k,0],traffic_line3a[k,4]])
                    if (mintot-tot).seconds<=43200:
                        transfer_bestline=[]
                        transfer_beststation=[]
                        mintot=tot
                        transfer_beststation.append(traffic_line1a[i,4])
                        transfer_beststation.append(traffic_line2a[j,4])
                        transfer_bestline.append(traffic_line1a[i,0])
                        transfer_bestline.append(traffic_line2a[j,0])
                        transfer_bestline.append(traffic_line3a[k,0])
                        
                        
# 计算最优换乘路线下的末班车时间         
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line3a)[0]):
        if data[i,0]==transfer_bestline[2] and data[i,1]==transfer_beststation[1]==traffic_line3a[j,3]:
            endtime_2=datetime.datetime.strptime(data[i,2],'%H:%M')
            
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line2a)[0]):
        for k in range(numpy.shape(data)[0]):
            if data[i,0]==transfer_bestline[1] and data[k,0]==transfer_bestline[2] and data[i,1]==transfer_beststation[0]==traffic_line2a[j,3] and transfer_beststation[1]==traffic_line2a[j,4]==data[k,1]:
                end_1=endtime_2-traffic_line2a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第一次换乘点的计算的末班车时间和实际第一次换乘点的末班车时间哪个在前               
for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[1] and data[i,1]==transfer_beststation[0]:
        endtime_1=min(datetime.datetime.strptime(data[i,2],'%H:%M'),end_1)            

for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line1a)[0]):
        for k in range(numpy.shape(data)[0]):
            if data[i,0]==transfer_bestline[0] and data[k,0]==transfer_bestline[1] and data[i,1]=='F'==traffic_line1a[j,3] and transfer_beststation[0]==traffic_line1a[j,4]==data[k,1]:
                end_0=endtime_1-traffic_line1a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第二次换乘点的计算的末班车时间和实际第二次换乘点的末班车时间哪个在前               
for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[0] and data[i,1]=='F':
        endtime_0=min(datetime.datetime.strptime(data[i,2],'%H:%M'),end_0)            

trafficstation=[]
trafficstation.append(start)
trafficstation.append(transfer_beststation[0])
trafficstation.append(transfer_beststation[1])
trafficstation.append(terminal)

timeend=[]
timeend.append(endtime_0.strftime('%H:%M'))
timeend.append(endtime_1.strftime('%H:%M'))
timeend.append(endtime_2.strftime('%H:%M'))

return(endtime,transfer_bestline,trafficstation,totusetime)














        