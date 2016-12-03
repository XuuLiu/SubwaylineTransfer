# SubwaylineTransfer
Calculate the shortest time of subway transfer, and get the last time of each transfer station
----------------------------------------------------------------------------------------------------------------------
Start of your journey: start
End of your journey: terminal
All subway lines that pass the start station: lines
All subway lines that pass the terminal station: linet

NO TRANSFER
If element a in lines and linet, then start and terminal station is on a same line, so we can get to terminal station from start station without transfer, and it’s the fastest way.

Total run time=the last arrive time of terminal- the last departure time of start
The last subway time at start=the last arrive time of start

------------------------------------------------------------------------------------------------------------------------

All subway station lines passed: start_station
All subway station linet passed: terminal_station

ONE TRANSFER
 
If element a in start_station and terminal_station，and a is the transfer station transfer1.

traffic_line1 contains [first-take subway line, net run time on this line, net run time on this line plus walk time to this line plus run interval of this line(Here equals to net run time, because this is the start), the start of this line, transfer station]

traffic_line2 contains [second-take subway line, net run time on this line, net run time on this line plus walk time to this line plus run interval of this line, transfer station, terminal]

totusetime contains total use time of all possible ways [total use time, start, first-take subway line, transfer1, second-take subway line, terminal]
transfer_beststation is the transfer station of the shortest used time line
transfer_bestline is the subway lines under the best circumstance
timeend is the last time under the best circumstance [the last time of start station, the last time of transfer1]

(the last time of start station= the last time of transfer1- interval of second-take subway line –transfer time on foot in the station)
if the last time of start station < the last time of start station on the time table:
	print the last time of start station
else:
	print the last time of start station on the time table
-------------------------------------------------------------------------------------------------------------------------
TWO TRANSFER
 
If element a in transfertwo_station and terminal_station, then a is the second transfer station transfertwostaion.

traffic_line1 contains [first-take subway line, net run time on this line, net run time on this line plus walk time to this line plus run interval of this line(Here equals to net run time, because this is the start), the start of this line, the first transfer station]

traffic_line2 contains [second-take subway line, net run time on this line, net run time on this line plus walk time to this line plus run interval of this line, the first transfer station, the second transfer station]

traffic_line3 contains [third-take subway line, net run time on this line, net run time on this line plus walk time to this line plus run interval of this line, the second transfer station, terminal]

totusetime contains total use time of all possible ways [total use time, start, first-take subway line, the first transfer station, second-take subway line, the second transfer station, third-take subway line, terminal]
transfer_beststation is the transfer station of the shortest used time line
transfer_bestline is the subway lines under the best circumstance

endtime_2 is the last time in the second transfer station, equals to the last arrival time of this station on the third-take subway line in the time table
endtime_1 is the last time in the first transfer station, equals to min[(endtime_2 minus the net run time of the second-take subway line minus the stop time of the third-take subway line at the second transfer station minus the transfer time in the second transfer station by foot minus the run interval of the third-take subway line), the last arrival time of the first transfer station on the second-take subway line in the time table ]
endtime_0 is the last time in the start station, equals to min[(endtime_1 minus the net run time of the first-take subway line minus the stop time of the second-take subway line at the first transfer station minus the transfer time in the first transfer station by foot minus the run interval of the second-take subway line), the last arrival time of the start station on the first-take subway line in the time table]]

timeend is the last time under the best circumstance [the last time of start station, the last time of the first transfer station, the last time of transfertwostaion]

-------------------------------------------------------------------------------------------------------------------------

THREE TRANSFER
 

similar
if element a in trans3_station and terminal_station, then a is the third transfer station.

----------------------------------------------------------------------------------------------------------------------------------- 

SHORTEST TOTAL RUN TIME 
If no transfer:
		Shortest
	Else if transfer once:
		If can transfer twice:
			Min(transfer once, transfer twice)
		Else:
			Transfer once
	Else if transfer twice:
		If can transfer three times:
			Min(transfer twice, transfer three times)
		Else:
			Transfer twice
	Else if transfer three times:
		Transfer three times
	Else:
		Ruturn[]

	







