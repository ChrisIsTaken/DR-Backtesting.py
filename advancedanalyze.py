import csv

#__________________________
Bear_ec_drmid = 0
Bear_ec_drmid_idrhigh = 0
Bear_ec_drmid_idrlow = 0
Bear_ec_drmid_idrlow_drmid = 0
Bear_ec_drmid_idrlow_drlow = 0
Bear_ec_drmid_idrhigh_idrlow = 0
Bear_ec_drmid_idrhigh_idrlow_drlow = 0
Bear_ec_drmid_idrhigh_idrlow_idrhigh = 0
#__________________________

ec_bearish_no_c_retraced_idr_high = 0
ec_bearish_no_c_retraced_idr_high_back_idr_low = 0
ec_bearish_no_c_retraced_dr_mid = 0
ec_bearish_no_c_retraced_dr_mid_back_idr_low = 0
ec_bearish_no_c_retraced_dr_mid_wicked_idr_high_back_idr_low = 0

ec_bullish_no_c_retraced_idr_low = 0
ec_bullish_no_c_retraced_idr_low_back_idr_high = 0
ec_bullish_no_c_retraced_dr_mid = 0

c_bearish_retraced_idr_high = 0
c_bearish_retraced_idr_high_back_idr_low = 0
c_bearish_retraced_dr_mid = 0
c_bearish_retraced_dr_mid_back_idr_low = 0
c_bearish_retraced_dr_mid_wicked_idr_high_back_idr_low = 0

c_bullish_retraced_idr_low = 0
c_bearish_retraced_idr_low_back_idr_high = 0
c_bearish_retraced_dr_mid_back_idr_high = 0
c_bearish_retraced_dr_mid_wicked_idr_low_back_idr_high = 0


# Open the CSV file
with open('sessions.csv', 'r') as sessions, open('breaks_candle.csv', 'r') as candlebreaks, open('breaks_wick.csv', 'r') as wickbreaks, open(r"data\USATECHIDXUSD.csv") as pricedata:
    readersession = csv.reader(sessions)
    readercandlebreaks = csv.reader(candlebreaks)
    readerwickbreaks = csv.reader(wickbreaks)
    readerprice = csv.reader(pricedata)

    #check for ec
    matched_break_rows = []
    
    for session_row in readersession:
        print(session_row)
         
        levels = [session_row[6], session_row[8], session_row[10], session_row[12], session_row[14]]
        level_map = {session_row[6]: 'idr_high', session_row[8]: 'dr_high', session_row[10]: 'dr_mid', session_row[12]: 'idr_low', session_row[14]: 'dr_low'}
    
        matched_break_rows = []
        matched_wick_rows = []

        print("session_row[-2]: ", session_row[-2])
        if session_row[-2] in ['3', '4']:
            print("sessions date: ", session_row[1])
            print("session validity times: ", session_row[4], session_row[5])
            print("entering for loop readercandlebreaks")
            for break_row in readercandlebreaks:
                #match the dates
                if session_row[1] == break_row[0]:

                    #Extract the time values at indexes 5 and 6
                    start_time = session_row[4]
                    end_time = session_row[5]

                    #Convert the time values to minutes past midnight
                    start_minutes = int(start_time[:2]) * 60 + int(start_time[3:])
                    end_minutes = int(end_time[:2]) * 60 + int(end_time[3:])

                    #Check if break is within relevant time
                    if start_minutes <= int(break_row[1][:2]) * 60 + int(break_row[1][3:]) <= end_minutes:
                        print("Breakrow:")
                        print(break_row)
                        matched_break_rows.append(break_row)

            for wick_row in readerwickbreaks:
                #match the dates

                if session_row[1] == wick_row[0]:

                    #Extract the time values at indexes 5 and 6
                    start_time = session_row[4]
                    end_time = session_row[5]

                    #Convert the time values to minutes past midnight
                    start_minutes = int(start_time[:2]) * 60 + int(start_time[3:])
                    end_minutes = int(end_time[:2]) * 60 + int(end_time[3:])

                    #Check if break is within relevant time
                    if start_minutes <= int(wick_row[1][:2]) * 60 + int(wick_row[1][3:]) <= end_minutes:
                        print("Wickrow:")
                        print(wick_row)
                        matched_wick_rows.append(wick_row)

        print("_________________________________________________")
        found_idr_high = False
        #checking sessions in which there were bear ec that held without confirmation
        print("1 session_row[-2]: ", session_row[-2])
        if (session_row[-2] == '3') or (session_row[-2] == '1'):

            #VERY IMPORTANT TO NOTE THAT IN THE FOLLOWING CASES PRICE NEVER CLOSED ABOVE DR_HIGH
            #BEARISH EC
            #checking if price retraced to idr high
            for matched_break in matched_break_rows:
	
                if (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                
                    found_idrlow = True

                if (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                
                    found_breakbelow_drlow = True

                if (found_idrlow == True) and (found_breakbelow_drlow != True) and (matched_break[2] == 'dr_mid' and matched_break[2] == '2'):
                
                    #Broke above DR Mid after IDR Low for the early indication without breaking DR Low
                    Bear_ec_drmid += 1

                    found_bear_ec_drmid = True


                if (found_bear_ec_drmid):
                
                    if (found_bear_ec_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                    
                        #Broke below IDR Low after previously breaking above DR Mid after bearish early indication
                        Bear_ec_drmid_idrlow += 1

                        found_bear_ec_drmid_idrlow = True

                    if (found_bear_ec_drmid_idrlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                    
                        #Broke above idrhigh after breaking above drmid  without going back to idrlow once again
                        Bear_ec_drmid_idrhigh += 1

                        found_bear_ec_drmid_idrhigh = True

                if (found_bear_ec_drmid_idrlow):
                
                    if (found_bear_ec_drmid_idrlow_drmid != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke below drlow after bear ec drmid idrlow
                        Bear_ec_drmid_idrlow_drlow += 1

                        found_bear_ec_drmid_idrlow_drlow = True

                    if (found_bear_ec_drmid_idrlow_drlow != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '2'):
                    
	            		#Broke above drmid after bear ec drmid idrlow
                        Bear_ec_drmid_idrlow_drmid += 1

                        found_bear_ec_drmid_idrlow_drmid = True

                if (found_bear_ec_drmid_idrhigh):
                
                    if (found_bear_ec_drmid_idrhigh_idrlow != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                    
	            		#Broke above DR High after previously confirming bearish early confirmation and breaking above DR Mid and IDR High
                        found_bear_ec_drmid_idrhigh_drhigh = True

                    if (found_bear_ec_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                    
	            		#Broke below IDR Low after bear ec drmid idrhigh 
                        Bear_ec_drmid_idrhigh_idrlow += 1

                        found_bear_ec_drmid_idrhigh_idrlow = True

                if (found_bear_ec_drmid_idrhigh_idrlow == True):
                
	            	#checking for times when after bear ec price went to idrhigh and down to drlow afterwards
                    if (found_bear_ec_drmid_idrhigh_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke below DR Low after bear ec drmid idrhigh idrlow
                        Bear_ec_drmid_idrhigh_idrlow_drlow += 1

                        found_bear_ec_drmid_idrhigh_idrlow_drlow = True

                    if (found_bear_ec_drmid_idrhigh_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):

                        #Broke above IDR High after bear ec drmid idrhigh idrlow
                        Bear_ec_drmid_idrhigh_idrlow_idrhigh += 1

                        found_bear_ec_drmid_idrhigh_idrlow_idrhigh = True

        elif (session_row[-2] == '4') or (session_row[-2] == '2'):

            #VERY IMPORTANT TO NOTE THAT IN THE FOLLOWING CASES PRICE NEVER CLOSED BELOW DR_LOW
            #BULLISH EC
            #checking if price retraced to idr high
            for matched_break in matched_break_rows:
	
                if (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                
                    found_idrhigh = True

                if (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                
                    found_breakabove_drhigh = True

                if (found_idrhigh == True) and (found_breakabove_drhigh != True) and (matched_break[2] == 'dr_mid' and matched_break[2] == '1'):
                
                    #Broke below DR Mid after IDR High for the early indication without breaking DR High
                    Bull_ec_drmid += 1

                    found_bull_ec_drmid = True


                if (found_bull_ec_drmid):
                
                    if (found_bull_ec_drmid_idrlow != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '2'):
                    
                        #Broke above IDR high after previously breaking below DR Mid after bullish early indication
                        Bull_ec_drmid_idrhigh += 1

                        found_bull_ec_drmid_idrhigh = True

                    if (found_bull_ec_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                    
                        #Broke above idrlow after breaking below drmid  without going back to idrhigh once again
                        Bull_ec_drmid_idrlow += 1

                        found_bull_ec_drmid_idrlow = True

                if (found_bull_ec_drmid_idrhigh):
                
                    if (found_bull_ec_drmid_idrhigh_drmid != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                    
	            		#Broke above drhigh after bull ec drmid idrhigh
                        Bull_ec_drmid_idrhigh_drhigh += 1

                        found_bbull_ec_drmid_idrhigh_drhigh = True

                    if (found_bull_ec_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '1'):
                    
	            		#Broke above drmid after bear ec drmid idrlow
                        Bull_ec_drmid_idrhigh_drmid += 1

                        found_bull_ec_drmid_idrhigh_drmid = True

                if (found_bull_ec_drmid_idrlow):
                
                    if (found_bull_ec_drmid_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke above DR High after previously confirming bearish early confirmation and breaking above DR Mid and IDR High
                        found_bull_ec_drmid_idrlow_drlow = True

                    if (found_bull_ec_drmid_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                    
	            		#Broke above IDR High after bull ec drmid idrlow 
                        Bull_ec_drmid_idrlow_idrhigh += 1

                        found_bull_ec_drmid_idrlow_idrhigh = True

                if (found_bull_ec_drmid_idrlow_idrhigh == True):
                
	            	#checking for times when after bull ec price went to idrlow and up to drhigh afterwards
                    if (found_bull_ec_drmid_idrlow_idrhigh_idrlow != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke below DR Low after bear ec drmid idrhigh idrlow
                        Bear_ec_drmid_idrlow_idrhigh_drhigh += 1

                        found_bear_ec_drmid_idrlow_idrhigh_drhigh = True

                    if (found_bull_ec_drmid_idrlow_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):

                        #Broke above IDR Low after bull ec drmid idrlow idrhigh
                        Bull_ec_drmid_idrlow_idrhigh_idrlow += 1

                        found_bull_ec_drmid_idrlow_idrhigh_idrlow = True