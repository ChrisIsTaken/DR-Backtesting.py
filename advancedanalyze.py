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

Bull_ec_drmid = 0
Bull_ec_drmid_idrhigh = 0
Bull_ec_drmid_idrlow = 0
Bull_ec_drmid_idrhigh_drhigh = 0
Bull_ec_drmid_idrhigh_drmid = 0
Bull_ec_drmid_idrlow_idrhigh = 0
Bull_ec_drmid_idrlow_idrhigh_drhigh = 0
Bull_ec_drmid_idrlow_idrhigh_idrlow = 0

Bear_c_drmid = 0
Bear_c_drmid_idrlow = 0
Bear_c_drmid_idrhigh = 0
Bear_c_drmid_idrlow_drlow = 0
Bear_c_drmid_idrlow_drmid = 0
Bear_c_drmid_idrhigh_idrlow = 0
Bear_c_drmid_idrhigh_idrlow_drlow = 0
Bear_c_drmid_idrhigh_idrlow_idrhigh = 0

Bull_c_drmid = 0
Bull_c_drmid_idrhigh = 0
Bull_c_drmid_idrlow = 0
Bull_c_drmid_idrhigh_drhigh = 0
Bull_c_drmid_idrhigh_drmid = 0
Bull_c_drmid_idrlow_idrhigh = 0
Bull_c_drmid_idrlow_idrhigh_drhigh = 0
Bull_c_drmid_idrlow_idrhigh_idrlow = 0
#__________________________

# Open the CSV file
with open('sessions.csv', 'r') as sessions, open('breaks_candle.csv', 'r') as candlebreaks, open('breaks_wick.csv', 'r') as wickbreaks, open(r"data\USATECHIDXUSD.csv") as pricedata:
    readersession = csv.reader(sessions)
    readercandlebreaks = csv.reader(candlebreaks)
    readerwickbreaks = csv.reader(wickbreaks)
    readerprice = csv.reader(pricedata)
    
    for session_row in readersession:
        #print("_________________________________________________")
        #print(session_row)
         
        candlebreaks.seek(0)
        wickbreaks.seek(0)
        pricedata.seek(0)
        
        levels = [session_row[6], session_row[8], session_row[10], session_row[12], session_row[14]]
        level_map = {session_row[6]: 'idr_high', session_row[8]: 'dr_high', session_row[10]: 'dr_mid', session_row[12]: 'idr_low', session_row[14]: 'dr_low'}
    
        matched_break_rows = []
        matched_wick_rows = []

        found_bear_ec_idrlow = False
        found_bear_ec_breakbelow_drlow = False
        found_bear_ec_drmid = False
        found_bear_ec_drmid_idrlow = False
        found_bear_ec_drmid_idrhigh = False
        found_bear_ec_drmid_idrlow_drlow = False
        found_bear_ec_drmid_idrlow_drmid = False
        found_bear_ec_drmid_idrhigh_drhigh = False
        found_bear_ec_drmid_idrhigh_idrlow = False
        found_bear_ec_drmid_idrhigh_idrlow_drlow = False
        found_bear_ec_drmid_idrhigh_idrlow_idrhigh = False

        found_bullish_ec_idrhigh = False
        found_bull_ec_breakabove_drhigh = False
        found_bull_ec_drmid = False
        found_bull_ec_idrhigh = False
        found_bull_ec_drmid_idrhigh = False
        found_bull_ec_drmid_idrlow = False
        found_bull_ec_drmid_idrhigh_drhigh = False
        found_bull_ec_drmid_idrhigh_drmid = False
        found_bull_ec_drmid_idrlow_drlow = False
        found_bull_ec_drmid_idrlow_idrhigh = False
        found_bull_ec_drmid_idrlow_idrhigh_drhigh = False
        found_bull_ec_drmid_idrlow_idrhigh_idrlow = False

        found_bear_ec_breakbelow_idrlow = False
        found_bear_ec_breakbelow_drlow = False
        found_bear_c_drmid = False
        found_bear_c_drmid_idrlow = False
        found_bear_c_drmid_idrhigh = False
        found_bear_c_drmid_idrlow_drlow = False
        found_bear_c_drmid_idrlow_drmid = False
        found_bear_c_drmid_idrhigh_drhigh = False
        found_bear_c_drmid_idrhigh_idrlow = False
        found_bear_c_drmid_idrhigh_idrlow_drlow = False
        found_bear_c_drmid_idrhigh_idrlow_idrhigh = False

        found_bull_c_idrhigh = False
        found_bull_c_breakabove_drhigh = False
        found_bull_c_drmid = False
        found_bull_c_drmid_idrhigh = False
        found_bull_c_drmid_idrlow = False
        found_bull_c_drmid_idrhigh_drhigh = False
        found_bull_c_drmid_idrhigh_drmid = False
        found_bull_c_drmid_idrlow_drlow = False
        found_bull_c_drmid_idrlow_idrhigh = False
        found_bull_c_drmid_idrlow_idrhigh_drhigh = False
        found_bull_c_drmid_idrlow_idrhigh_idrlow = False

        #print("session_row[-2]: ", session_row[-2])
        #if session_row[-2] in [3, 4]:
        #print("sessions date: ", session_row[1])
        #print("session validity times: ", session_row[4], session_row[5])
        #print("entering for loop readercandlebreaks")
        for break_row in readercandlebreaks:
            #match the dates
            #print("session_row[1]", session_row[1])
            #print("break_row[0]", break_row[0])
            if session_row[1] == break_row[0]:

                #Extract the time values at indexes 5 and 6
                start_time = session_row[4]
                end_time = session_row[5]

                #Convert the time values to minutes past midnight
                start_minutes = int(start_time[:2]) * 60 + int(start_time[3:])
                end_minutes = int(end_time[:2]) * 60 + int(end_time[3:])

                #Check if break is within relevant time
                if start_minutes <= int(break_row[1][:2]) * 60 + int(break_row[1][3:]) <= end_minutes:
                    #print("Breakrow:")
                    #print(break_row)
                    matched_break_rows.append(break_row)

        #for wick_row in readerwickbreaks:
        #    #match the dates
#
        #    if session_row[1] == wick_row[0]:
#
        #        #Extract the time values at indexes 5 and 6
        #        start_time = session_row[4]
        #        end_time = session_row[5]
#
        #        #Convert the time values to minutes past midnight
        #        start_minutes = int(start_time[:2]) * 60 + int(start_time[3:])
        #        end_minutes = int(end_time[:2]) * 60 + int(end_time[3:])
#
        #        #Check if break is within relevant time
        #        if start_minutes <= int(wick_row[1][:2]) * 60 + int(wick_row[1][3:]) <= end_minutes:
        #            #print("Wickrow:")
        #            #print(wick_row)
        #            matched_wick_rows.append(wick_row)

        #print("1 session_row[-2]:", session_row[-2])
        #print("matched_break_rows")
        #print(matched_break_rows)
        if session_row[-2] in ['1', '3']:
            #print("if session_row[-2] in ['3', '4']:")

            #VERY IMPORTANT TO NOTE THAT IN THE FOLLOWING CASES PRICE NEVER CLOSED ABOVE DR_HIGH
            #BEARISH EC
            #checking for the dr low break
            print("__________")
            for matched_break in matched_break_rows:
                #print("entering matched_break loop")

                #print("matched_break[2]", matched_break[2])
                #print("matched_break[4]", matched_break[4])
                if (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                    #print("found_bear_ec_idrlow TRUE")
                    found_bear_ec_idrlow = True

                if (found_bear_ec_idrlow) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    print("found_bear_ec_breakbelow_drlow TRUE")
                    found_bear_ec_breakbelow_drlow = True
                    print("#########")
                    print(found_bear_ec_idrlow, found_bear_ec_breakbelow_drlow, matched_break[2], matched_break[4])
                    print("#########")
                if (found_bear_ec_idrlow == True) and (found_bear_ec_breakbelow_drlow != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '2'):
                    print("Bear_ec_drmid +1")
                    #Broke above DR Mid after IDR Low for the early indication without breaking DR Low
                    Bear_ec_drmid += 1

                    found_bear_ec_drmid = True


                if (found_bear_ec_drmid):
                    print("found_bear_ec_drmid")
                    print(found_bear_ec_drmid_idrhigh, matched_break[2], matched_break[4])
                    if (found_bear_ec_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bear_ec_drmid_idrlow += 1")
                        #Broke below IDR Low after previously breaking above DR Mid after bearish early indication
                        Bear_ec_drmid_idrlow += 1

                        found_bear_ec_drmid_idrlow = True

                    if (found_bear_ec_drmid_idrlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bear_ec_drmid_idrhigh += 1")
                        #Broke above idrhigh after breaking above drmid  without going back to idrlow once again
                        Bear_ec_drmid_idrhigh += 1

                        found_bear_ec_drmid_idrhigh = True

                if (found_bear_ec_drmid_idrlow):
                    print("++++++++++++")
                    print(found_bear_ec_drmid_idrlow_drmid, matched_break[2], matched_break[4])
                    if (found_bear_ec_drmid_idrlow_drmid != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bear_ec_drmid_idrlow_drlow += 1")
	            		#Broke below drlow after bear ec drmid idrlow
                        Bear_ec_drmid_idrlow_drlow += 1

                        found_bear_ec_drmid_idrlow_drlow = True

                    print(found_bear_ec_drmid_idrlow_drlow, matched_break[2], matched_break[4])
                    if (found_bear_ec_drmid_idrlow_drlow != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '2'):
                        print("Bear_ec_drmid_idrlow_drmid += 1")
	            		#Broke above drmid after bear ec drmid idrlow
                        Bear_ec_drmid_idrlow_drmid += 1

                        found_bear_ec_drmid_idrlow_drmid = True

                if (found_bear_ec_drmid_idrhigh):
                
                    if (found_bear_ec_drmid_idrhigh_idrlow != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                    
	            		#Broke above DR High after previously confirming bearish early confirmation and breaking above DR Mid and IDR High
                        found_bear_ec_drmid_idrhigh_drhigh = True

                    if (found_bear_ec_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bear_ec_drmid_idrhigh_idrlow += 1")
	            		#Broke below IDR Low after bear ec drmid idrhigh 
                        Bear_ec_drmid_idrhigh_idrlow += 1

                        found_bear_ec_drmid_idrhigh_idrlow = True

                if (found_bear_ec_drmid_idrhigh_idrlow == True):
                
	            	#checking for times when after bear ec price went to idrhigh and down to drlow afterwards
                    if (found_bear_ec_drmid_idrhigh_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bear_ec_drmid_idrhigh_idrlow_drlow += 1")
	            		#Broke below DR Low after bear ec drmid idrhigh idrlow
                        Bear_ec_drmid_idrhigh_idrlow_drlow += 1

                        found_bear_ec_drmid_idrhigh_idrlow_drlow = True

                    if (found_bear_ec_drmid_idrhigh_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bear_ec_drmid_idrhigh_idrlow_idrhigh += 1")
                        #Broke above IDR High after bear ec drmid idrhigh idrlow
                        Bear_ec_drmid_idrhigh_idrlow_idrhigh += 1

                        found_bear_ec_drmid_idrhigh_idrlow_idrhigh = True
        print("session_row[-2] before bull ec", session_row[-2])
        if session_row[-2] in ['2', '4']:
            #print("if session_row[-2] in ['4', '2']:")

            #VERY IMPORTANT TO NOTE THAT IN THE FOLLOWING CASES PRICE NEVER CLOSED BELOW DR_LOW
            #BULLISH EC
            #checking if price retraced to idr high
            for matched_break in matched_break_rows:

                if (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                    found_bull_ec_idrhigh = True

                if (found_bull_ec_idrhigh) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                    print("found_bull_ec_breakabove_drhigh TRUE")
                    found_bull_ec_breakabove_drhigh = True
                    print("#########")
                    print(found_bull_ec_idrhigh, found_bull_ec_breakabove_drhigh, matched_break[2], matched_break[4])
                    print("#########")
                if (found_bull_ec_idrhigh == True) and (found_bull_ec_breakabove_drhigh != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '1'):
                    print("Bull_ec_drmid +1")
                    #Broke above DR Mid after IDR Low for the early indication without breaking DR Low
                    Bull_ec_drmid += 1

                    found_bull_ec_drmid = True


                if (found_bull_ec_drmid):
                
                    if (found_bull_ec_drmid_idrlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bull_ec_drmid_idrhigh += 1")
                        #Broke above IDR high after previously breaking below DR Mid after bullish early indication
                        Bull_ec_drmid_idrhigh += 1

                        found_bull_ec_drmid_idrhigh = True

                    if (found_bull_ec_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bull_ec_drmid_idrlow += 1")
                        #Broke above idrlow after breaking below drmid  without going back to idrhigh once again
                        Bull_ec_drmid_idrlow += 1

                        found_bull_ec_drmid_idrlow = True

                if (found_bull_ec_drmid_idrhigh):
                
                    if (found_bull_ec_drmid_idrhigh_drmid != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                        print("Bull_ec_drmid_idrhigh_drhigh += 1")
	            		#Broke above drhigh after bull ec drmid idrhigh
                        Bull_ec_drmid_idrhigh_drhigh += 1

                        found_bull_ec_drmid_idrhigh_drhigh = True

                    if (found_bull_ec_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '1'):
                        print("Bull_ec_drmid_idrhigh_drmid += 1")
	            		#Broke above drmid after bear ec drmid idrlow
                        Bull_ec_drmid_idrhigh_drmid += 1

                        found_bull_ec_drmid_idrhigh_drmid = True

                if (found_bull_ec_drmid_idrlow):
                
                    if (found_bull_ec_drmid_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke above DR High after previously confirming bearish early confirmation and breaking above DR Mid and IDR High
                        found_bull_ec_drmid_idrlow_drlow = True

                    if (found_bull_ec_drmid_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bull_ec_drmid_idrlow_idrhigh += 1")
	            		#Broke above IDR High after bull ec drmid idrlow 
                        Bull_ec_drmid_idrlow_idrhigh += 1

                        found_bull_ec_drmid_idrlow_idrhigh = True

                if (found_bull_ec_drmid_idrlow_idrhigh == True):
                
	            	#checking for times when after bull ec price went to idrlow and up to drhigh afterwards
                    if (found_bull_ec_drmid_idrlow_idrhigh_idrlow != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bull_ec_drmid_idrlow_idrhigh_drhigh += 1")
	            		#Broke below DR Low after bear ec drmid idrhigh idrlow
                        Bull_ec_drmid_idrlow_idrhigh_drhigh += 1

                        found_bull_ec_drmid_idrlow_idrhigh_drhigh = True

                    if (found_bull_ec_drmid_idrlow_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bull_ec_drmid_idrlow_idrhigh_idrlow += 1")
                        #Broke above IDR Low after bull ec drmid idrlow idrhigh
                        Bull_ec_drmid_idrlow_idrhigh_idrlow += 1

                        found_bull_ec_drmid_idrlow_idrhigh_idrlow = True

        if session_row[-1] in ['1', '3']:
            #print("if session_row[-1] in ['3', '1']:")

            #VERY IMPORTANT TO NOTE THAT IN THE FOLLOWING CASES PRICE NEVER CLOSED ABOVE DR_HIGH
            #BEARISH C
            for matched_break in matched_break_rows:

                #essentially you are checking for a idrlow followed by drlow
                #therefore you check for the break below idrlow and for the drlow breaks in order to search for drmid also checking if idrlow has been found already in the drlow check in order for the sequence to be right
	
                if (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                    print("found_bear_ec_breakbelow_idrlow = True")
                    found_bear_ec_breakbelow_idrlow = True

                if (found_bear_ec_breakbelow_idrlow == True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    print("found_bear_ec_breakbelow_drlow = True")
                    found_bear_ec_breakbelow_drlow = True

                print("***************")
                print(found_bear_ec_breakbelow_idrlow, found_bear_ec_breakbelow_drlow, matched_break[2], matched_break[4])
                if (found_bear_ec_breakbelow_idrlow == True) and (found_bear_ec_breakbelow_drlow == True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '2'):
                    print("Bear_c_drmid += 1")
                    #Broke above DR Mid after IDR Low and DR Low for the confirmation
                    Bear_c_drmid += 1

                    found_bear_c_drmid = True


                if (found_bear_c_drmid):
                    print("''''''''''''''''")
                    print(found_bear_c_drmid_idrhigh, matched_break[2], matched_break[4])
                    if (found_bear_c_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bear_c_drmid_idrlow += 1")
                        #Broke below IDR Low after previously breaking above DR Mid after bearish early indication and confirmation
                        Bear_c_drmid_idrlow += 1

                        found_bear_c_drmid_idrlow = True

                    if (found_bear_c_drmid_idrlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bear_c_drmid_idrhigh += 1")
                        #Broke above idrhigh after breaking above drmid without going back to idrlow once again
                        Bear_c_drmid_idrhigh += 1

                        found_bear_c_drmid_idrhigh = True

                if (found_bear_c_drmid_idrlow):
                
                    if (found_bear_c_drmid_idrlow_drmid != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bear_c_drmid_idrlow_drlow += 1")
	            		#Broke below drlow after bear c drmid idrlow
                        Bear_c_drmid_idrlow_drlow += 1

                        found_bear_c_drmid_idrlow_drlow = True

                    if (found_bear_c_drmid_idrlow_drlow != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '2'):
                        print("Bear_c_drmid_idrlow_drmid += 1")
	            		#Broke above drmid after bear c drmid idrlow
                        Bear_c_drmid_idrlow_drmid += 1

                        found_bear_c_drmid_idrlow_drmid = True

                if (found_bear_c_drmid_idrhigh):
                
                    if (found_bear_c_drmid_idrhigh_idrlow != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                    
	            		#Broke above DR High after previous bearish confirmation and breaking above DR Mid and IDR High (essentially breaking confirmation)
                        found_bear_c_drmid_idrhigh_drhigh = True

                    if (found_bear_c_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bear_c_drmid_idrhigh_idrlow += 1")
	            		#Broke below IDR Low after bear ec drmid idrhigh 
                        Bear_c_drmid_idrhigh_idrlow += 1

                        found_bear_c_drmid_idrhigh_idrlow = True

                if (found_bear_c_drmid_idrhigh_idrlow == True):
                    print("------------", found_bear_c_drmid_idrhigh_idrlow_idrhigh, matched_break[2], matched_break[4])
	            	#checking for times when after bear c price went to idrhigh and down to drlow afterwards
                    if (found_bear_c_drmid_idrhigh_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bear_c_drmid_idrhigh_idrlow_drlow += 1")
	            		#Broke below DR Low after bear c drmid idrhigh idrlow
                        Bear_c_drmid_idrhigh_idrlow_drlow += 1

                        found_bear_c_drmid_idrhigh_idrlow_drlow = True
                    print("~~~~~~~~~~~", found_bear_c_drmid_idrhigh_idrlow_drlow, matched_break[2], matched_break[4])
                    if (found_bear_c_drmid_idrhigh_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bear_c_drmid_idrhigh_idrlow_idrhigh += 1")
                        #Broke above IDR High after bear c drmid idrhigh idrlow
                        Bear_c_drmid_idrhigh_idrlow_idrhigh += 1

                        found_bear_c_drmid_idrhigh_idrlow_idrhigh = True

        if session_row[-1] in ['2', '4']:
            #print("if session_row[-1] in ['4', '2']:")

            #BULLISH C
            #checking if price retraced to idr high
            for matched_break in matched_break_rows:
	
                #essentially you are checking for a idrhigh followed by drhigh
                #therefore you check for the break above idrhigh and for the drhigh breaks in order to search for drmid also checking if idrhigh has been found already in the drhigh check in order for the sequence to be right
                print(":::::::::::::", matched_break[2], matched_break[4])
                if (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                
                    found_bull_c_idrhigh = True
                print(";;;;;;;;;", found_bull_c_idrhigh, matched_break[2], matched_break[4])
                if (found_bull_c_idrhigh == True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                
                    found_bull_c_breakabove_drhigh = True

                if (found_bull_c_idrhigh == True) and (found_bull_c_breakabove_drhigh == True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '1'):
                    print("Bull_c_drmid += 1")
                    #Broke below DR Mid after IDR High for the early indication without breaking DR High
                    Bull_c_drmid += 1

                    found_bull_c_drmid = True


                if (found_bull_c_drmid):
                
                    if (found_bull_c_drmid_idrlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bull_c_drmid_idrhigh += 1")
                        #Broke above IDR high after previously breaking above DR Mid after bullish early indication and confirmation
                        Bull_c_drmid_idrhigh += 1

                        found_bull_c_drmid_idrhigh = True

                    if (found_bull_c_drmid_idrhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bull_c_drmid_idrlow += 1")
                        #Broke below idrlow after breaking above drmid without going back to idrhigh once again
                        Bull_c_drmid_idrlow += 1

                        found_bull_c_drmid_idrlow = True

                if (found_bull_c_drmid_idrhigh):
                
                    if (found_bull_c_drmid_idrhigh_drmid != True) and (matched_break[2] == 'dr_high') and (matched_break[4] == '2'):
                        print("Bull_c_drmid_idrhigh_drhigh += 1")
	            		#Broke above drhigh after bull c drmid idrhigh
                        Bull_c_drmid_idrhigh_drhigh += 1

                        found_bull_c_drmid_idrhigh_drhigh = True

                    if (found_bull_c_drmid_idrhigh_drhigh != True) and (matched_break[2] == 'dr_mid') and (matched_break[4] == '1'):
                        print("Bull_c_drmid_idrhigh_drmid += 1")
	            		#Broke above drmid aft er bull c drmid idrlow
                        Bull_c_drmid_idrhigh_drmid += 1

                        found_bull_c_drmid_idrhigh_drmid = True

                if (found_bull_c_drmid_idrlow):
                
                    if (found_bull_c_drmid_idrlow_idrhigh != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                    
	            		#Broke above DR High after previously confirming bull early confirmation and confirmation and breaking below DR Mid and IDR High
                        found_bull_c_drmid_idrlow_drlow = True

                    if (found_bull_c_drmid_idrlow_drlow != True) and (matched_break[2] == 'idr_high') and (matched_break[4] == '2'):
                        print("Bull_c_drmid_idrlow_idrhigh += 1")
	            		#Broke above IDR High after bull c drmid idrlow 
                        Bull_c_drmid_idrlow_idrhigh += 1

                        found_bull_c_drmid_idrlow_idrhigh = True

                if (found_bull_c_drmid_idrlow_idrhigh == True):
                
	            	#checking for times when after bull c price went to idrlow and up to drhigh afterwards
                    if (found_bull_c_drmid_idrlow_idrhigh_idrlow != True) and (matched_break[2] == 'dr_low') and (matched_break[4] == '1'):
                        print("Bull_c_drmid_idrlow_idrhigh_drhigh += 1")
	            		#Broke below DR Low after bear c drmid idrhigh idrlow
                        Bull_c_drmid_idrlow_idrhigh_drhigh += 1

                        found_bull_c_drmid_idrlow_idrhigh_drhigh = True

                    if (found_bull_c_drmid_idrlow_idrhigh_drhigh != True) and (matched_break[2] == 'idr_low') and (matched_break[4] == '1'):
                        print("Bull_c_drmid_idrlow_idrhigh_idrlow += 1")
                        #Broke above IDR Low after bull c drmid idrlow idrhigh
                        Bull_c_drmid_idrlow_idrhigh_idrlow += 1

                        found_bull_c_drmid_idrlow_idrhigh_idrlow = True


    #Calculate probabilities
    #print("Calculating probabilities")

    #BEAR EC:
    #Probability of price retracing straight to idrlow after price went to idrhigh after bearish early indication
    Bear_ec_drmid_idrhigh_idrlow_percentage = (Bear_ec_drmid_idrhigh_idrlow / Bear_ec_drmid_idrhigh) * 100
    print(f"Probability of price retracing straight to idrlow after price went to idrhigh after bearish early indication: {Bear_ec_drmid_idrhigh_idrlow_percentage:.2f}%")

    #Probability of price retracing straight down to drlow past idrlow after price went to idrhigh after bearish early indication
    Bear_ec_drmid_idrhigh_idrlow_drlow_percentage = (Bear_ec_drmid_idrhigh_idrlow_drlow / Bear_ec_drmid_idrhigh)
    print(f"Probability of price retracing straight down to drlow past idrlow after price went to idrhigh after bearish early indication: {Bear_ec_drmid_idrhigh_idrlow_drlow_percentage:.2f}%")

    #Probability that price closes below drlow after price closed below idrlow after bearish early indication and price going up to idrhigh
    Bear_ec_drmid_idrhigh_idrlow_drlow_after_idrlow_percentage = (Bear_ec_drmid_idrhigh_idrlow_drlow / Bear_ec_drmid_idrhigh_idrlow)
    print(f"Probability that price closes below drlow after price closed below idrlow after bearish early indication and price going up to idrhigh: {Bear_ec_drmid_idrhigh_idrlow_drlow_after_idrlow_percentage:.2f}%")

    #print("______________________________________________")

    #BULL EC
    #Probability of price retracing straight to idrhigh after price went to idrlow after bullish early indication
    Bull_ec_drmid_idrlow_idrhigh_percentage = (Bull_ec_drmid_idrlow_idrhigh / Bull_ec_drmid_idrlow) * 100
    print(f"Probability of price retracing straight to idrhigh after price went to idrlow after bullish early indication: {Bull_ec_drmid_idrlow_idrhigh_percentage:.2f}%")

    #Probability of price retracing straight up to drhigh past idrhigh after price went to idrlow after bullish early indication
    Bull_ec_drmid_idrlow_idrhigh_drhigh_percentage = (Bull_ec_drmid_idrlow_idrhigh_drhigh / Bull_ec_drmid_idrlow)
    print(f"Probability of price retracing straight up to drhigh past idrhigh after price went to idrlow after bullish early indication: {Bull_ec_drmid_idrlow_idrhigh_drhigh_percentage:.2f}%")

    #Probability that price closes above drhigh after price closed above idrhigh after bull early indication and price going fown to idrlow
    Bull_ec_drmid_idrlow_idrhigh_drhigh_after_idrhigh_percentage = (Bull_ec_drmid_idrlow_idrhigh_drhigh / Bull_ec_drmid_idrlow_idrhigh)
    print(f"Probability that price closes above drhigh after price closed above idrhigh after bull early indication and price going fown to idrlow: {Bull_ec_drmid_idrlow_idrhigh_drhigh_after_idrhigh_percentage:.2f}%")

    #print("______________________________________________")

    #BEAR C:
    #Probability of price retracing straight to idrlow after price went to idrhigh after bearish confirmation
    Bear_c_drmid_idrhigh_idrlow_percentage = (Bear_c_drmid_idrhigh_idrlow / Bear_c_drmid_idrhigh) * 100
    print(f"Probability of price retracing straight to idrlow after price went to idrhigh after bearish confirmation: {Bear_c_drmid_idrhigh_idrlow_percentage:.2f}%")

    #Probability of price retracing straight down to drlow past idrlow after price went to idrhigh after bearish confirmation
    Bear_c_drmid_idrhigh_idrlow_drlow_percentrage = (Bear_c_drmid_idrhigh_idrlow_drlow / Bear_c_drmid_idrhigh) * 100
    print(f"Probability of price retracing straight down to drlow past idrlow after price went to idrhigh after bearish confirmation: {Bear_c_drmid_idrhigh_idrlow_drlow_percentrage:.2f}%")

    #Probability that price closes below drlow after price closed below idrlow after bearish confirmation and price going up to idrhigh
    Bear_c_drmid_idrhigh_idrlow_after_idrlow_percentage = (Bear_c_drmid_idrhigh_idrlow_drlow / Bear_c_drmid_idrhigh_idrlow)
    print(f"Probability that price closes below drlow after price closed below idrlow after bearish confirmation and price going up to idrhigh: {Bear_c_drmid_idrhigh_idrlow_after_idrlow_percentage:.2f}%")

    #print("______________________________________________")

    #BULL C:
    #Probability of price retracing straight to idrhigh after price went to idrlow after bullish early indicaiton
    Bull_c_drmid_idrlow_idrhigh_percentage = (Bull_c_drmid_idrlow_idrhigh / Bull_c_drmid_idrlow) * 100
    print(f"Probability of price retracing straight to idrhigh after price went to idrlow after bullish early indicaiton: {Bull_c_drmid_idrlow_idrhigh_percentage:.2f}%")

    #Probability of price retracing straight up to drhigh past idrhigh after price went to idrlow after bullish confirmation
    Bull_c_drmid_idrlow_idrhigh_drhigh_percentage = (Bull_c_drmid_idrlow_idrhigh_drhigh / Bull_c_drmid_idrlow)
    print(f"Probability of price retracing straight up to drhigh past idrhigh after price went to idrlow after bullish confirmation: {Bull_c_drmid_idrlow_idrhigh_drhigh_percentage:.2f}%")

    #Probability that price closes above drhigh after price closed above idrhigh after bull early indication and price going down to idrlow
    Bull_c_drmid_idrlow_idrhigh_drhigh_after_idrhigh_percentage = (Bull_c_drmid_idrlow_idrhigh_drhigh / Bull_c_drmid_idrlow_idrhigh)
    print(f"Probability that price closes above drhigh after price closed above idrhigh after bull early indication and price going down to idrlow: {Bull_c_drmid_idrlow_idrhigh_drhigh_after_idrhigh_percentage:.2f}%")