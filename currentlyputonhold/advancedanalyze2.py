import csv
import datetime

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

with open('sessions.csv', 'r') as sessions:
    readersession = csv.DictReader(sessions)
    session_dict = {}
    for i, session_row in enumerate(readersession):
        print(session_row)
        session_dict[i] = session_row[1]

#Read breaks data into list
with open('breaks_candle.csv', 'r') as candlebreaks:
    readercandlebreaks = csv.DictReader(candlebreaks)
    break_dict = {}
    for i, break_row in enumerate(readercandlebreaks):
        break_dict[i] = break_row[0]


#Create nested dictionary to store break rows for each session
session_breaks_dict = {}
for session_key, session_value in session_dict.items():
    session_date = session_value['session_date']
    session_start_time = session_value['session_start_time']
    session_end_time = session_value['session_end_time']

    # Filter the breaks for this session
    session_breaks = {}
    for break_key, break_value in break_dict.items():
        if break_value['session_date'] == session_date \
                and session_start_time <= break_value['break_start_time'] <= session_end_time:
            session_breaks[break_key] = break_value

    # Add the filtered breaks to the session_breaks_dict
    session_breaks_dict[session_key] = session_breaks

print(session_breaks_dict)

# Read price data into list
#with open(r"data\USATECHIDXUSD.csv") as pricedata:
#    readerprice = csv.DictReader(pricedata)
#    pricedata_list = [price_row for price_row in readerprice]

#for session_key, session_value in session_dict.items():
#    session_date = session_value[1]
#    session_start_time = datetime.strptime(session_value[2], '%H:%M')
#    session_end_time = datetime.strptime(session_value[3], '%H:%M')
#    
#    # filter the breaks for this session using list comprehension
#    session_breaks = [break_value for break_key, break_value in break_dict.items() 
#                      if break_value[2] == session_date 
#                      and session_start_time <= datetime.strptime(break_value[1], '%H:%M') <= session_end_time]