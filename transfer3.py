# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:40:36 2016

@author: XuLiu
"""

trans2_line,trans2_station=startline_station(data,start_station,lines)

trans3_line,trans3_station=startline_station(data,trans2_station,trans2_line)
        
transfer3s=[]#第三次换乘的车站
for i in range(numpy.shape(terminal_station)[0]):
    for j in range(numpy.shape(trans3_station)[0]):
        if terminal_station[i]==trans3_station[j]:
            transfer3s.append(trans3_station[j])
transfer3station=unique(transfer3s)

transfer3l=[]#第三次乘坐的线           
for m in transfer3station:
    for n in trans2_station:
        for i in range(numpy.shape(data)[0]):
            for j in range(numpy.shape(data)[0]):
                if data[i,1]==m and data[j,1]==n and data[i,0]==data[j,0]:
                    transfer3l.append(data[i,0])
transfer3line=unique(transfer3l)

transfer2s=[]#第二次换乘的车站
for i in range(numpy.shape(transfer3line)[0]):
    for j in range(numpy.shape(trans2_station)[0]):
        for k in range(numpy.shape(data)[0]):
            if transfer3line[i]==data[k,0] and trans2_station[j]==data[k,1]:
                transfer2s.append(trans2_station[j])
transfer2station=unique(transfer2s)
    


transfer2l=[]#第二次乘坐的线           
for m in transfer2station:
    for n in start_station:
        for i in range(numpy.shape(data)[0]):
            for j in range(numpy.shape(data)[0]):
                if data[i,1]==m and data[j,1]==n and data[i,0]==data[j,0]:
                    transfer2l.append(data[i,0])
transfer2line=unique(transfer2l)

transfer1s=[]#第一次换乘的车站
for i in range(numpy.shape(transfer2line)[0]):
    for j in range(numpy.shape(start_station)[0]):
        for k in range(numpy.shape(data)[0]):
            if transfer2line[i]==data[k,0] and start_station[j]==data[k,1]:
                transfer1s.append(start_station[j])
transfer1station=unique(transfer1s)

#######################################计算运行时间
traffic_line1=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer1station)[0]):
            if data[m,1]==transfer1station[k] and data[n,1]=='E' and data[m,0]==data[n,0]:
                runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                if runtime0.seconds<43200:
                    traffic_line1.append([data[m,0],runtime0,runtime0,'E',start_station[k]])#第一次乘车的线名称
traffic_line1a=numpy.array(traffic_line1)

traffic_line2=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer2station)[0]):
            for l in range(numpy.shape(traffic_line1a)[0]):
                if data[m,1]==transfer2station[k] and data[n,1]==traffic_line1a[l,4] and data[m,0]==data[n,0]:
                    runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime1.seconds<43200:
                        runtime1tot=runtime1+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                        traffic_line2.append([data[m,0],runtime1,runtime1tot,traffic_line1a[l,4],transfer2station[k]])#第二次乘车的线名称
traffic_line2a=numpy.array(traffic_line2)

traffic_line3=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer3station)[0]):
            for l in range(numpy.shape(traffic_line2a)[0]):
                if data[m,1]==transfer3station[k] and data[n,1]==traffic_line2a[l,4] and data[m,0]==data[n,0]:
                    runtime2=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime2.seconds<43200:
                        runtime2tot=runtime2+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                        traffic_line3.append([data[m,0],runtime2,runtime2tot,traffic_line2a[l,4],transfer3station[k]])#第二次乘车的线名称
traffic_line3a=numpy.array(traffic_line3)

traffic_line4=[]
for m in range(numpy.shape(data)[0]):
    for n in range(numpy.shape(data)[0]):
        for k in range(numpy.shape(transfer3station)[0]):
            if data[m,1]=='F' and data[n,1]==transfer3station[k] and data[m,0]==data[n,0]:
                runtime3=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                if runtime3.seconds<43200:
                    runtime3tot=runtime3+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                    traffic_line4.append([data[m,0],runtime3,runtime3tot,transfer3station[k],'F'])#第三次乘车的线名称
traffic_line4a=numpy.array(traffic_line4)

    #求所有路径的耗时，与得到最优换乘路线：
totusetime=[]

mintot=traffic_line1a[0,2]+traffic_line2a[0,2]+traffic_line3a[0,2]+traffic_line4a[0,2]
for i in range(numpy.shape(traffic_line1a)[0]):
    for j in range(numpy.shape(traffic_line2a)[0]):
        for k in range(numpy.shape(traffic_line3a)[0]):
            for l in range(numpy.shape(traffic_line4a)[0]):
                if traffic_line1a[i,4]==traffic_line2a[j,3]:
                    if traffic_line2a[j,4]==traffic_line3a[k,3]:
                        if traffic_line3a[k,4]==traffic_line4a[l,3]:
                            tot=traffic_line1a[i,2]+traffic_line2a[j,2]+traffic_line3a[k,2]+traffic_line4a[l,2]
                            totusetime.append([(tot.seconds/60),traffic_line1a[i,3],traffic_line1a[i,0],traffic_line2a[j,3],traffic_line2a[j,0],traffic_line3a[k,3],traffic_line3a[k,0],traffic_line3a[k,4],traffic_line4a[l,0],traffic_line4a[l,4]])
                            if (mintot-tot).seconds<43200:
                                transfer_bestline=[]
                                transfer_beststation=[]
                                mintot=tot
                                transfer_beststation.append(traffic_line1a[i,4])
                                transfer_beststation.append(traffic_line2a[j,4])
                                transfer_beststation.append(traffic_line3a[k,4])
                                transfer_bestline.append(traffic_line1a[i,0])
                                transfer_bestline.append(traffic_line2a[j,0])
                                transfer_bestline.append(traffic_line3a[k,0])
                                transfer_bestline.append(traffic_line4a[l,0])
# 计算最优换乘路线下的末班车时间  
# 倒数第二站末班车
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line4a)[0]):
        if data[i,0]==transfer_bestline[3] and data[i,1]==transfer_beststation[2]==traffic_line4a[j,3]:
            endtime_3=datetime.datetime.strptime(data[i,2],'%H:%M')
#倒数第三站末班车
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line3a)[0]):
        for k in range(numpy.shape(data)[0]):
            if data[i,0]==transfer_bestline[2] and data[k,0]==transfer_bestline[3] and data[i,1]==transfer_beststation[1]==traffic_line3a[j,3] and transfer_beststation[2]==traffic_line3a[j,4]==data[k,1]:
                end_2=endtime_3-traffic_line3a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第二次换乘点的计算的末班车时间和实际第一次换乘点的末班车时间哪个在前               
for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[2] and data[i,1]==transfer_beststation[1]:
        endtime_2=min(datetime.datetime.strptime(data[i,2],'%H:%M'),end_2) 
##倒数第四站，即第二站的末班车
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line2a)[0]):
        for k in range(numpy.shape(data)[0]):
            if data[i,0]==transfer_bestline[1] and data[k,0]==transfer_bestline[2] and data[i,1]==transfer_beststation[0]==traffic_line2a[j,3] and transfer_beststation[1]==traffic_line2a[j,4]==data[k,1]:
                end_1=endtime_2-traffic_line2a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第一次换乘点的计算的末班车时间和实际第一次换乘点的末班车时间哪个在前               
for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[1] and data[i,1]==transfer_beststation[0]:
        endtime_1=min(datetime.datetime.strptime(data[i,2],'%H:%M'),end_1) 
#出发站末班车        
for i in range(numpy.shape(data)[0]):
    for j in range(numpy.shape(traffic_line1a)[0]):
        for k in range(numpy.shape(data)[0]):
            if data[i,0]==transfer_bestline[0] and data[k,0]==transfer_bestline[1] and data[i,1]=='E'==traffic_line1a[j,3] and transfer_beststation[0]==traffic_line1a[j,4]==data[k,1]:
                end_0=endtime_1-traffic_line1a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第二次换乘点的计算的末班车时间和实际第二次换乘点的末班车时间哪个在前               
for i in range(numpy.shape(data)[0]):
    if data[i,0]==transfer_bestline[0] and data[i,1]=='E':
        endtime_0=min(datetime.datetime.strptime(data[i,2],'%H:%M'),end_0)  


trafficstation=[]
trafficstation.append(start)
trafficstation.append(transfer_beststation[0])
trafficstation.append(transfer_beststation[1])
trafficstation.append(transfer_beststation[2])
trafficstation.append(terminal)

timeend=[]
timeend.append(endtime_0.strftime('%H:%M'))
timeend.append(endtime_1.strftime('%H:%M'))
timeend.append(endtime_2.strftime('%H:%M'))
timeend.append(endtime_3.strftime('%H:%M'))


return(timeend,transfer_bestline,trafficstation,totusetime)












