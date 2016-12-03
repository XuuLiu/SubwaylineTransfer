# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 20:10:56 2016

@author: XuLiu
"""
#-*-coding:utf-8 -*-
#!/usr/bin/env python

import numpy
import datetime

def loadDataSet(fileName):   #读取文件，txt文档
    numFeat = len(open(fileName,'r',encoding='gbk').readline().split('\t')) #自动检测特征的数目
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):      
            lineArr.append(curLine[i])
        dataMat.append(lineArr)
    return dataMat

def unique(old_list):#去重
    newList = []
    for x in old_list:
        if x not in newList :
            newList.append(x)
    return newList


def trafficline(data,start,terminal):#看经过起点终点的交通线，data格式：交通线，站
    ls=[]#经过出发点的交通线
    lt=[]#经过终点的交通线
    for i in range(numpy.shape(data)[0]):
        if data[i,1]==start:
            ls.append(data[i,0])
        if data[i,1]==terminal:
            lt.append(data[i,0])
    return unique(ls),unique(lt)

def transfer0(data,start,terminal,lines,linet):#无换乘时计算末班车时间,即出发站末班车时间-出发站内步行时间-运行间隔
    timeend=[]#末班车的时间
    runtime=[]#运行时间
    traffic_line=[]#乘坐的交通线
    traffic_station=[start,terminal]#停止的站，不换乘时为终点与起点，换乘时包括换乘站
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):
            for k in range(numpy.shape(data)[0]):
                if lines[i]==linet[j]==data[k,0] and data[k,1]==start:
                    for a in range(numpy.shape(data)[0]):
                        if lines[i]==linet[j]==data[a,0] and data[a,1]==terminal:
                            delta=datetime.datetime.strptime(data[a,2],'%H:%M')-datetime.datetime.strptime(data[k,2],'%H:%M')
                            if delta.seconds<=43200:
                                timeend.append(data[k,2])
                                runtime.append(numpy.int((datetime.datetime.strptime(data[a,2],'%H:%M')-datetime.datetime.strptime(data[k,3],'%H:%M')).seconds/60))
                                traffic_line.append(data[k,0])
    return(timeend,runtime,traffic_line,traffic_station)

#某地铁线经过的所有点的集合，排除已知点
def station(data,line,station_excld):
    ss=[]
    for i in range(numpy.shape(line)[0]):
        for j in range(numpy.shape(data)[0]):
            if line[i]==data[j,0] and data[j,1]!=station_excld:
                ss.append(data[j,1])
    return(unique(ss))

#看是否符合一次换乘的情况
def whethertransfer1(startstation,terminalstation):
    a=[]      
    for i in range(numpy.shape(startstation)[0]):
        for j in range(numpy.shape(terminalstation)[0]):
            if startstation[i]==terminalstation[j]:
                a.append('T')
            else:
                a.append('F')
    if 'T' in a:
        return('T')
                
#一次换乘的换乘站
#一次换乘时计算时间与时间最短路线
def transfer1(data,start_station,terminal_station,start,terminal):
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
                if data[m,1]==transfer1[k] and data[n,1]==start and data[m,0]==data[n,0]:
                    runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime0.seconds<=43200:
                        traffic_line1.append([data[m,0],runtime0,runtime0,start,transfer1[k]])#第一次乘车的线名称
    traffic_line1a=numpy.array(traffic_line1)
                    
    traffic_line2=[]                    
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(transfer1)[0]):
                if data[m,1]==terminal and data[n,1]==transfer1[k] and data[m,0]==data[n,0]:
                    runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')#纯运行时间
                    if runtime1.seconds<=43200:
                        runtime1tot=runtime1+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))
                        traffic_line2.append([data[m,0],runtime1,runtime1tot,transfer1[k],terminal])#第二次乘车的线名称 
    traffic_line2a=numpy.array(traffic_line2)
                    
    #求所有路径的耗时，与得到最优换乘路线：
    totusetime=[]#所有可行路线的集合
    mintot=datetime.timedelta(0,43200)
    for i in range(numpy.shape(traffic_line1a)[0]):
        for j in range(numpy.shape(traffic_line2a)[0]):
            if traffic_line1a[i,4]==traffic_line2a[j,3]:
                tot=traffic_line1a[i,2]+traffic_line2a[j,2]
                totusetime.append([tot.seconds/60,traffic_line1a[i,3],traffic_line1a[i,0],traffic_line1a[i,4],traffic_line2a[j,0],traffic_line2a[j,4]])
                if (mintot-tot).seconds<=43200:
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
            if transfer_bestline[1]==data[i,0]==data[j,0] and data[i,1]==transfer_beststation[0] and data[j,1]==terminal:
                end1=datetime.datetime.strptime(data[i,2],'%H:%M')-datetime.timedelta(minutes=numpy.int(data[i,4]))-datetime.timedelta(minutes=numpy.int(data[i,5]))
                timeend.append(end1.strftime('%H:%M'))
                timeend.append(data[i,2])
###以上为正常计算末班车时间，第二个地铁线换乘站的末班时间-换乘时间-运行间隔-换乘之前的地铁运行时间
#出发站的末班车时间
    trafficstation=[]
    trafficstation.append(start)
    trafficstation.append(transfer_beststation[0])
    trafficstation.append(terminal)
    start_endtime=[]
    for i in range(numpy.shape(data)[0]):
        if data[i,0]==transfer_bestline[0] and data[i,1]==start:
            start_endtime.append(data[i,2])
    if timeend[0]<=start_endtime[0]:
        return(timeend,transfer_bestline,trafficstation,totusetime)
    else:
        start_endtime.append(timeend[1])
        return(start_endtime,transfer_bestline,trafficstation,totusetime)


        

###一下为考虑两次换乘的函数
def startline_station(data,ss,ls):#看经过起点的地铁线经过的地铁站，经过这些地铁站还有哪些线,然后这些线经过的点,即看出发点换乘一次可以达到的所有的地铁站                
    lts=[]
    for i in range(unique(numpy.shape(ss))[0]):
        for j in range(numpy.shape(data)[0]):
            if ss[i]==data[j,1] and data[j,0] not in ls:
                lts.append(data[j,0])
    ltss=[]#看上一条线还过哪些点
    for i in range(unique(numpy.shape(lts))[0]):
        for j in range(numpy.shape(data)[0]):
            if lts[i]==data[j,0] and data[j,1]:
                ltss.append(data[j,1])
    return(unique(lts),unique(ltss))


#判断是否换乘两次
def whethertransfertwo(data,start_station,lines,terminal_station):
    transfertwo_line,transfertwo_station=startline_station(data,start_station,lines)
    transfertwos=[]#第二次换乘的车站
    for i in range(numpy.shape(terminal_station)[0]):
        for j in range(numpy.shape(transfertwo_station)[0]):
            if terminal_station[i]==transfertwo_station[j]:
                transfertwos.append(transfertwo_station[j])
    transfertwoss=unique(transfertwos)

    transfertwol=[]#第二次乘坐的线           
    for m in transfertwos:
        for n in start_station:
            for i in range(numpy.shape(data)[0]):
                for j in range(numpy.shape(data)[0]):
                    if data[i,1]==m and data[j,1]==n and data[i,0]==data[j,0]:
                        transfertwol.append(data[i,0])
    poss_transfers_two=[]
    for i in range(numpy.shape(terminal_station)[0]):
        for j in range(numpy.shape(transfertwoss)[0]):
            if terminal_station[i]==transfertwoss[j]:
                poss_transfers_two.append(transfertwoss[j])
            
    if poss_transfers_two==[]:
        return('F')
    else:
        return('T')
        
        
####计算换乘两次的最优路径以及末班车时间：
def transfer2(data,start,terminal,start_station,terminal_station,lines,linet):
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
            
            
#其中runtimetot都包括此段的运行时间与上一段到此段的步行时间与运行间隔
    traffic_line1=[]
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(start_station)[0]):
                if data[m,1]==start_station[k] and data[n,1]==start and data[m,0]==data[n,0]:
                    runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime0.seconds<=43200:
                        traffic_line1.append([data[m,0],runtime0,runtime0,start,start_station[k]])#第一次乘车的线名称
    traffic_line1a=numpy.array(traffic_line1)

    traffic_line2=[]
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(transfertwostation)[0]):
                for l in range(numpy.shape(traffic_line1a)[0]):
                    if data[m,1]==transfertwostation[k] and data[n,1]==traffic_line1a[l,4] and data[m,0]==data[n,0]:
                        runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                        if runtime1.seconds<=43200:
                            runtime1tot=runtime1+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                            traffic_line2.append([data[m,0],runtime1,runtime1tot,traffic_line1a[l,4],transfertwostation[k]])#第二次乘车的线名称
    traffic_line2a=numpy.array(traffic_line2)


    traffic_line3=[]
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(transfertwostation)[0]):
                if data[m,1]==terminal and data[n,1]==transfertwostation[k] and data[m,0]==data[n,0]:
                    runtime2=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime2.seconds<=43200:
                        runtime2tot=runtime2+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                        traffic_line3.append([data[m,0],runtime2,runtime2tot,transfertwostation[k],terminal])#第三次乘车的线名称
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
                if data[i,0]==transfer_bestline[0] and data[k,0]==transfer_bestline[1] and data[i,1]==start==traffic_line1a[j,3] and transfer_beststation[0]==traffic_line1a[j,4]==data[k,1]:
                    end_0=endtime_1-traffic_line1a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第二次换乘点的计算的末班车时间和实际第二次换乘点的末班车时间哪个在前               
    for i in range(numpy.shape(data)[0]):
        if data[i,0]==transfer_bestline[0] and data[i,1]==start:
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

    return(timeend,transfer_bestline,trafficstation,totusetime)


def whethertransfer3(data,start_station,terminal_station,lines):
    trans2_line,trans2_station=startline_station(data,start_station,lines)
    trans3_line,trans3_station=startline_station(data,trans2_station,trans2_line)
        
    transfer3s=[]#第三次换乘的车站
    for i in range(numpy.shape(terminal_station)[0]):
        for j in range(numpy.shape(trans3_station)[0]):
            if terminal_station[i]==trans3_station[j]:
                transfer3s.append(trans3_station[j])
    transfer3station=unique(transfer3s)
    if transfer3station!=[]:
        return('T')
    else:
        return('F')
    


def transfer3(data,start,terminal,start_station,terminal_station,lines,linet):
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
                if data[m,1]==transfer1station[k] and data[n,1]==start and data[m,0]==data[n,0]:
                    runtime0=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime0.seconds<=43200:
                        traffic_line1.append([data[m,0],runtime0,runtime0,start,start_station[k]])#第一次乘车的线名称
    traffic_line1a=numpy.array(traffic_line1)

    traffic_line2=[]
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(transfer2station)[0]):
                for l in range(numpy.shape(traffic_line1a)[0]):
                    if data[m,1]==transfer2station[k] and data[n,1]==traffic_line1a[l,4] and data[m,0]==data[n,0]:
                        runtime1=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                        if runtime1.seconds<=43200:
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
                        if runtime2.seconds<=43200:
                            runtime2tot=runtime2+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                            traffic_line3.append([data[m,0],runtime2,runtime2tot,traffic_line2a[l,4],transfer3station[k]])#第二次乘车的线名称
    traffic_line3a=numpy.array(traffic_line3)

    traffic_line4=[]
    for m in range(numpy.shape(data)[0]):
        for n in range(numpy.shape(data)[0]):
            for k in range(numpy.shape(transfer3station)[0]):
                if data[m,1]==terminal and data[n,1]==transfer3station[k] and data[m,0]==data[n,0]:
                    runtime3=datetime.datetime.strptime(data[m,2],'%H:%M')-datetime.datetime.strptime(data[n,3],'%H:%M')
                    if runtime3.seconds<=43200:
                        runtime3tot=runtime3+datetime.timedelta(minutes=numpy.int(data[n,4]))+datetime.timedelta(minutes=numpy.int(data[n,5]))+(datetime.datetime.strptime(data[n,3],'%H:%M')-datetime.datetime.strptime(data[n,2],'%H:%M'))
                        traffic_line4.append([data[m,0],runtime3,runtime3tot,transfer3station[k],terminal])#第三次乘车的线名称
    traffic_line4a=numpy.array(traffic_line4)

    #求所有路径的耗时，与得到最优换乘路线：
    totusetime=[]

    mintot=datetime.timedelta(0,43200)
    for i in range(numpy.shape(traffic_line1a)[0]):
        for j in range(numpy.shape(traffic_line2a)[0]):
            for k in range(numpy.shape(traffic_line3a)[0]):
                for l in range(numpy.shape(traffic_line4a)[0]):
                    if traffic_line1a[i,4]==traffic_line2a[j,3]:
                        if traffic_line2a[j,4]==traffic_line3a[k,3]:
                            if traffic_line3a[k,4]==traffic_line4a[l,3]:
                                tot=traffic_line1a[i,2]+traffic_line2a[j,2]+traffic_line3a[k,2]+traffic_line4a[l,2]
                                totusetime.append([(tot.seconds/60),traffic_line1a[i,3],traffic_line1a[i,0],traffic_line2a[j,3],traffic_line2a[j,0],traffic_line3a[k,3],traffic_line3a[k,0],traffic_line3a[k,4],traffic_line4a[l,0],traffic_line4a[l,4]])
                                if (mintot-tot).seconds<=43200:
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
                if data[i,0]==transfer_bestline[0] and data[k,0]==transfer_bestline[1] and data[i,1]==start==traffic_line1a[j,3] and transfer_beststation[0]==traffic_line1a[j,4]==data[k,1]:
                    end_0=endtime_1-traffic_line1a[j,1]-(datetime.datetime.strptime(data[i,3],'%H:%M')-datetime.datetime.strptime(data[i,2],'%H:%M'))-datetime.timedelta(minutes=numpy.int(data[k,4]))-datetime.timedelta(minutes=numpy.int(data[k,5]))

#判断第二次换乘点的计算的末班车时间和实际第二次换乘点的末班车时间哪个在前               
    for i in range(numpy.shape(data)[0]):
        if data[i,0]==transfer_bestline[0] and data[i,1]==start:
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




def end_time(data,start,terminal):    
#lines为过出发点经过的地铁线，linet为过终点经过的地铁线
    lines,linet=trafficline(data,start,terminal)
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):
            if lines[i]==linet[j]:#不用换乘的情况
                timeend_transfer0,runtime0,traffic_line0,traffic_station0=transfer0(data,start,terminal,lines,linet)
                return(timeend_transfer0,traffic_line0,traffic_station0,runtime0)
    start_station=station(data,lines,start)#经过出发点的地铁线还经过的地铁站
    terminal_station=station(data,linet,terminal)#经过终点的地铁线还经过的地铁站
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):
            if whethertransfer1(start_station,terminal_station)=='T' and whethertransfertwo(data,start_station,lines,terminal_station)=='T':
            #经过出发点的地铁线经过的地铁站中有经过终点的地铁线还经过的地铁站种一样的地铁站,即换乘一次
                timeend_transfer1,traffic_line1,traffic_station1,runtime1=transfer1(data,start_station,terminal_station,start,terminal)
                timeend_transfer2,traffic_line2,traffic_station2,runtime2=transfer2(data,start,terminal,start_station,terminal_station,lines,linet)
                if min(numpy.array(runtime1)[:,0])<=min(numpy.array(runtime2)[:,0]):
                    return(timeend_transfer1,traffic_line1,traffic_station1,[runtime1,runtime2])
                else:
                    return(timeend_transfer2,traffic_line2,traffic_station2,[runtime1,runtime2])
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):
            if whethertransfer1(start_station,terminal_station)=='T':
                timeend_transfer1,traffic_line1,traffic_station1,runtime1=transfer1(data,start_station,terminal_station,start,terminal)
                return(timeend_transfer1,traffic_line1,traffic_station1,runtime1)
                
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):
            if whethertransfertwo(data,start_station,lines,terminal_station)=='T' and whethertransfer3(data,start_station,terminal_station,lines)=='T':#换乘两次
                timeend_transfer2,traffic_line2,traffic_station2,runtime2=transfer2(data,start,terminal,start_station,terminal_station,lines,linet)
                timeend_transfer3,traffic_line3,traffic_station3,runtime3=transfer3(data,start,terminal,start_station,terminal_station,lines,linet)
                if min(numpy.array(runtime2)[:,0])<=min(numpy.array(runtime3)[:,0]):
                    return(timeend_transfer2,traffic_line2,traffic_station2,[runtime2,runtime3])
                else:
                    return(timeend_transfer3,traffic_line3,traffic_station3,[runtime2,runtime3])
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):                    
            if whethertransfertwo(data,start_station,lines,terminal_station)=='T':
                timeend_transfer2,traffic_line2,traffic_station2,runtime2=transfer2(data,start,terminal,start_station,terminal_station,lines,linet)
                return(timeend_transfer2,traffic_line2,traffic_station2,runtime2)                    
    for i in range(numpy.shape(lines)[0]):
        for j in range(numpy.shape(linet)[0]):                    
            if whethertransfer3(data,start_station,terminal_station,lines)=='T':
                timeend_transfer3,traffic_line3,traffic_station3,runtime3=transfer3(data,start,terminal,start_station,terminal_station,lines,linet)
                return(timeend_transfer3,traffic_line3,traffic_station3,runtime3)
    return([],[],[],[])
 
def laststation(data):
    last_station=[]
    last_s=[]
    unique_line=[]
    unique_line.append(data[0,0])
    for i in range(numpy.shape(data)[0]):
        if data[i,0] not in unique_line:
            unique_line.append(data[i,0])
    for j in range(numpy.shape(unique_line)[0]):
        oneline=[]
        for i in range(numpy.shape(data)[0]):
            if data[i,0]==unique_line[j]:
                oneline.append(data[i,1])
        last_s.append(oneline[0])
        last_s.append(oneline[-1])
            
    last_station=unique(last_s) 
    return(last_station) 
    
def end_fnl(data,start):
    for t in laststation(data):
        if t!=start:
            timeend_transfer,traffic_line,traffic_station,runtime=end_time(data,start,t) ###数据名称、起点、终点                  
            print(timeend_transfer,traffic_line,traffic_station,runtime)       
##################################################################################更改以下    
data=numpy.array(loadDataSet('/Users/XuLiu/Desktop/taobao3/tt_1.txt'))
#读取数据文件txt，其中第一列为地铁线名称，第二列为站名，第三列为此站的末班时间，第四列为此站内换乘耗时，第五列为此线的运行间隔
end_fnl(data,'西门口')##输入数据名称和起点

           
            

 


