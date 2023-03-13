import pandas as pd
import csv
from datetime import datetime
import subprocess

from backtesting import Strategy, Backtest

class Session:
    def __init__(self, session_name, date, defining_hour_start, defining_hour_end, session_validity, dr_high, dr_high_timestamp, dr_low, dr_low_timestamp, idr_high, idr_high_timestamp, idr_low, idr_low_timestamp, dr_mid, earlyindication, confirmation):
        #self.session_id = session_id
        self.session_name = session_name
        self.date = date
        self.defining_hour_start = defining_hour_start
        self.defining_hour_end = defining_hour_end
        self.session_validity = session_validity
        self.dr_high = dr_high
        self.dr_high_timestamp = dr_high_timestamp
        self.dr_low = dr_low
        self.dr_low_timestamp = dr_low_timestamp
        self.idr_high = idr_high
        self.idr_high_timestamp = idr_high_timestamp
        self.idr_low = idr_low
        self.idr_low_timestamp = idr_low_timestamp
        self.drmid = dr_mid
        self.earlyindication = earlyindication
        self.confirmation = confirmation

class Levelbreak():
    def __init__(self, date, time, levelname, level, result, open, close, volume):
        #self.session_id = session_id
        self.date = date
        self.time = time
        self.levelname = levelname
        self.level = level
        self.result = result
        self.open = open
        self.close = close
        self.volume = volume

#Loading data from CSV file into the dataframe that is to be passed to backtesting.py
data = pd.read_csv(r"data\datasample.csv", names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

breakinstances = []
sessioninstances = []

def is_time_between(time, start, end):

    #Convert times to number of minutes
    time = int(time[:2]) * 60 + int(time[3:])
    start = int(start[:2]) * 60 + int(start[3:])
    end = int(end[:2]) * 60 + int(end[3:])

    #Adjust end time if it is earlier than start time
    if end < start:
        end += 1440

    #Adjust time if it is before start time
    if time < start:
        time += 1440

    #Check if time is between start and end
    return start <= time <= end

#function to detect breaks in relevant levels
def breaklevel(open_price, close_price, level):
    if (open_price > level) and (close_price < level):
        return 1
    if (open_price < level) and (close_price > level):
        return 2

class DR_Backtesting(Strategy):
    def init(self):
        #print("running init")
        self.breaklist = []
        self.openlist = []
        self.closelist = []
        self.highlist = []
        self.lowlist = []

        self.drhourflag = False
        self.drlow = ''
        self.drhigh = ''
        self.idrlow = ''
        self.idrhigh = ''
        self.drmid = ''
        self.drlowtimestamp = ''
        self.drhightimestamp = ''
        self.idrlowtimestamp = ''
        self.idrhightimestamp = ''

        self.earlyindication = 0    #0 is just the default value that is to be overridden respectively meaning that it didnt happen
        self.confirmation = 0

        self.rdr_session = {
            'session_name': 'RDR',                          #Var to store the sessions name
            'defining_hour_start': "09:30",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "10:30",                   #Var to store time when session's defining hour ends
            'session_validity': "16:00",                    #Var to store time when session is invalid
        }

        self.adr_session = {
            'session_name': 'ADR',                          #Var to store the sessions name
            'defining_hour_start': "19:30",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "20:30",                   #Var to store time when session's defining hour ends
            'session_validity': "02:00",                    #Var to store time when session is invalid
        }

        self.odr_session = {
            'session_name': 'ODR',                          #Var to store the sessions name
            'defining_hour_start': "03:00",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "04:00",                   #Var to store time when session's defining hour ends
            'session_validity': "08:30",                    #Var to store time when session is invalid
        }
    

    def next(self):
        #print("running next()")
        for sessions in [self.rdr_session, self.adr_session, self.odr_session]:
            #print("running session: ", sessions['session_name'])
            #check if session has yet to be identified
            if is_time_between(self.data.Time[-1], sessions['defining_hour_start'], sessions['defining_hour_end']):
                #print("istimebetween dhstart dhend; updating levels")
                self.openlist.append((self.data.Open[-1], self.data.Time[-1]))
                self.closelist.append((self.data.Close[-1], self.data.Time[-1]))
                self.highlist.append((self.data.High[-1], self.data.Time[-1]))
                self.lowlist.append((self.data.Low[-1], self.data.Time[-1]))

                #Update levels and timestamps
                self.drhigh, self.drhightimestamp = max(self.openlist + self.closelist + self.highlist, key=lambda x: x[0])
                self.drlow, self.drlowtimestamp = min(self.openlist + self.closelist + self.lowlist, key=lambda x: x[0])
                self.idrlow, self.idrlowtimestamp = min(self.openlist + self.closelist, key=lambda x: x[0])
                self.idrhigh, self.idrhightimestamp = max(self.openlist + self.closelist, key=lambda x: x[0])

                self.drmid = 0.5 * (self.drhigh + self.drlow)

                #Checking if all the levels have values
                if self.drhigh != '' and self.drlow != '' and self.idrlow != '' and self.idrhigh != '':
                    self.drhourflag = True
            
            else:

                #Session's DR has been indetified, check if it's still valid
                if (self.drhourflag == True) and (is_time_between(self.data.Time[-1], sessions['defining_hour_end'], sessions['session_validity'])):
                    #print("if self.drhigh != '' and time between dhend and sessionvalidity")
                    levels = [self.drhigh, self.idrhigh, self.drmid, self.idrlow, self.drlow]
                    level_map = {self.drhigh: 'dr_high', self.idrhigh: 'idr_high', self.drmid: 'dr_mid', self.idrlow: 'idr_low', self.drlow: 'dr_low'}
                    
                    for level in levels:
                        
                        levelname = level_map.get(level)
                        #print(levelname)

                        result = breaklevel(self.data.Open[-1], self.data.Close[-1], level)
                        
                        if result != None:
                            #print("entered if breaklevel with following values: ", self.data.Open[-1], self.data.Close[-1], level)
                            #print("Result = ", result)

                            breakinstances.append(Levelbreak(self.data.Date[-1], self.data.Time[-1], levelname, level, result, self.data.Open[-1], self.data.Close[-1], self.data.Volume[-1]))
                            self.breaklist.append([self.data.Date[-1], self.data.Time[-1], levelname, level, result, self.data.Open[-1], self.data.Close[-1], self.data.Volume[-1]])

                    if (self.data.Time[-1] == sessions['session_validity']):

                        #print("time == sessionvalidity")
                        #print(self.breaklist)
                        #checking for early indication
                        for breakinstance in self.breaklist:
                            if breakinstance[2] == 'idr_high': #checks if early indication is bullish
                                #print("early indication is bullish")
                                found_dr_low = False
                                for breakinstance in self.breaklist:
                                    if breakinstance[2] == 'dr_low': # early indication has been bullish but broke
                                        #print("early indication has been bullish but broke")
                                        self.earlyindication = 2
                                        found_dr_low = True
                                        break
                                    
                                if found_dr_low == False: # early indication has been bullish and held true
                                    #print("early indication has been bullish and held")
                                    self.earlyindication = 4
                                break
                                    
                            elif breakinstance[2] == 'idr_low': #checks if early indication is bearish
                                #print("early indication is bearish")
                                found_dr_high = False
                                for breakinstance in self.breaklist:
                                    if breakinstance[2] == 'dr_high': #early indication has been bearish but broke
                                        #print("early indication has been bearish but broke")
                                        self.earlyindication = 1
                                        found_dr_high = True
                                        break
                                    
                                if found_dr_high == False: #early indication has been bearish and held true
                                    #print("early indication has been bearish and held")
                                    self.earlyindication = 3
                                break

                        #checking for confirmation
                        for breakinstance in self.breaklist:
                            if breakinstance[2] == 'dr_high': #checks if confirmation is bullish
                                #print("confirmation has been bullish")
                                found_dr_low = False
                                for breakinstance in self.breaklist:
                                    if breakinstance[2] == 'dr_low': #confirmation has been bullish but broke
                                        #print("confirmation has been bullish but broke")
                                        self.confirmation = 2
                                        found_dr_low = True
                                        break
                                    
                                if not found_dr_low: # confirmation has been bullish and held true
                                    #print("confirmation has been bullish and held")
                                    self.confirmation = 4
                                #break

                            elif breakinstance[2] == 'dr_low': #checks if confirmation is bearish
                                #print("confirmation has been bearish")
                                found_dr_high = False
                                for breakinstance in self.breaklist:
                                    if breakinstance[2] == 'dr_high': #confirmation has been bearish but broke
                                        #print("confirmation has been bearish but broke")
                                        self.confirmation = 1
                                        found_dr_high = True
                                        break

                                if found_dr_high == False: #early indication has been bearish and held true
                                    #print("confirmation has been bearish and held")
                                    self.confirmation = 3
                                #break

                        #print(sessions['session_name'], self.data.Date[-1], sessions['defining_hour_start'], sessions['defining_hour_end'], sessions['session_validity'], self.drhigh, self.drhightimestamp, self.drlow, self.drlowtimestamp, self.idrhigh, self.idrhightimestamp, self.idrlow, self.idrlowtimestamp, self.drmid, self.earlyindication, self.confirmation)
                        sessioninstances.append(Session(sessions['session_name'], self.data.Date[-1], sessions['defining_hour_start'], sessions['defining_hour_end'], sessions['session_validity'], self.drhigh, self.drhightimestamp, self.drlow, self.drlowtimestamp, self.idrhigh, self.idrhightimestamp, self.idrlow, self.idrlowtimestamp, self.drmid, self.earlyindication, self.confirmation))

                        self.breaklist = []
                        self.breakinstances = []
                        self.breaklist = []
                        self.openlist = []
                        self.closelist = []
                        self.highlist = []
                        self.lowlist = []

                        self.drhourflag = False
                        self.drlow = ''
                        self.drhigh = ''
                        self.idrlow = ''
                        self.idrhigh = ''
                        self.drlowtimestamp = ''
                        self.drhightimestamp = ''
                        self.idrlowtimestamp = ''
                        self.idrhightimestamp = ''
                        self.drmid = ''

                        self.idr_high_broken = False
                        self.idr_low_broken = False
                        self.dr_high_broken = False
                        self.dr_low_broken = False
                        self.earlyindication = 0
                        self.confirmation = 0

# Create a Backtest object using the data and the strategy
bt = Backtest(data, DR_Backtesting, cash=100000, commission=.000)
stats = bt.run()

#Export dataframes to CSV
dfsessions = pd.DataFrame([t.__dict__ for t in sessioninstances])
dfbreaks = pd.DataFrame([t.__dict__ for t in breakinstances])

with open('sessions.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dfsessions.columns.tolist())
    writer.writeheader = False
    writer.writerows(dfsessions.to_dict(orient='records'))

with open('breaks.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dfbreaks.columns.tolist())
    writer.writeheader = False
    writer.writerows(dfbreaks.to_dict(orient='records'))

subprocess.run(["python", "analyze.py"])