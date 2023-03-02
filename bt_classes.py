import pandas as pd
import csv
from datetime import datetime
import subprocess

from backtesting import Strategy, Backtest

class Session:
    def __init__(self, session_name, date, defining_hour_start, defining_hour_end, session_validity, dr_high, dr_high_timestamp, dr_low, dr_low_timestamp, idr_high, idr_high_timestamp, idr_low, idr_low_timestamp, dr_mid, ec, rule):
        #self.session_id = session_id
        self.session_name = session_name
        self.date = date
        self.defining_hour_start = defining_hour_start
        self.defining_hour_end = defining_hour_end
        session_validity = session_validity
        self.dr_high = dr_high
        self.dr_high_timestamp = dr_high_timestamp
        self.dr_low = dr_low
        self.dr_low_timestamp = dr_low_timestamp
        self.idr_high = idr_high
        self.idr_high_timestamp = idr_high_timestamp
        self.idr_low = idr_low
        self.idr_low_timestamp = idr_low_timestamp
        self.dr_mid = dr_mid
        self.ec = ec
        self.rule = rule

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
data = pd.read_csv(r"data\USATECHIDXUSD.csv", names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

data['timestamp'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%Y.%m.%d %H:%M')
#are those two lines below even neccesary?
data['hour'] = data['timestamp'].dt.hour
data['minute'] = data['timestamp'].dt.minute

breakinstances = []
sessioninstances = []

def is_time_between(time, start, end):

     # Convert times to number of minutes
    time = int(time[:2]) * 60 + int(time[3:])
    start = int(start[:2]) * 60 + int(start[3:])
    end = int(end[:2]) * 60 + int(end[3:])

    # Adjust end time if it is earlier than start time
    if end < start:
        end += 1440

    # Adjust time if it is before start time
    if time < start:
        time += 1440

    # Check if time is between start and end, accounting for spans over midnight
    return start <= time <= end

#function to detect breaks in relevant levels
def breaklevel(open_price, close_price, level):
    if (open_price > level) and (close_price < level):
        return 1
    if (open_price < level) and (close_price > level):
        return 2

class DR_Backtesting(Strategy):
    def init(self):

        self.breaklist = []
        self.drhourflag = False
        self.drlow = ''
        self.drhigh = ''
        self.idrlow = ''
        self.idrhigh = ''
        self.dr_mid = ''
        self.drlowtimestamp = ''
        self.drhightimestamp = ''
        self.idrlowtimestamp = ''
        self.idrhightimestamp = ''

        self.idr_high_broken = False
        self.idr_low_broken = False
        self.dr_high_broken = False
        self.dr_low_broken = False
        self.ec = True
        self.rule = True

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

        for sessions in [self.rdr_session, self.adr_session, self.odr_session]:

            #check if session has yet to be identified
            if is_time_between(self.data.Time[-1], sessions['defining_hour_start'], sessions['defining_hour_end']):
                
                if 'openlist' in locals():
                    openlist.append((self.data.Open[-1], self.data.Time[-1]))
                else: openlist = [(self.data.Open[-1], self.data.Time[-1])]
                if 'closelist' in locals():
                    closelist.append((self.data.Close[-1], self.data.Time[-1]))
                else: closelist = [(self.data.Close[-1], self.data.Time[-1])]
                if 'highlist' in locals():
                    highlist.append((self.data.High[-1], self.data.Time[-1]))
                else: highlist = [(self.data.High[-1], self.data.Time[-1])]
                if 'lowlist' in locals():
                    lowlist.append((self.data.Low[-1], self.data.Time[-1]))
                else: lowlist = [(self.data.Low[-1], self.data.Time[-1])]

                #Update levels and timestamps
                self.drhigh, self.drhightimestamp = max(openlist + closelist + highlist, key=lambda x: x[0])
                self.drlow, self.drlowtimestamp = min(openlist + closelist + lowlist, key=lambda x: x[0])
                self.idrlow, self.idrlowtimestamp = min(openlist + closelist, key=lambda x: x[0])
                self.idrhigh, self.idrhightimestamp = max(openlist + closelist, key=lambda x: x[0])

                self.dr_mid = 0.5 * (self.drhigh + self.drlow)
            
            else:

                #Session's DR has been indetified, check if it's still valid
                if (self.drhigh != '') and (is_time_between(self.data.Time[-1], sessions['defining_hour_end'], sessions['session_validity'])):
                    
                    levels = [self.drlow, self.drhigh, self.idrlow, self.idrhigh, self.dr_mid]
                    
                    for level in levels:

                        levelname = None
                        if level == self.drlow: levelname = 'dr_low'
                        if level == self.drhigh: levelname = 'dr_high'
                        if level == self.idrlow: levelname = 'idr_low'
                        if level == self.idrhigh: levelname = 'idr_high'
                        if level == self.dr_mid: levelname = 'dr_mid'

                        result = breaklevel(self.data.Open[-1], self.data.Close[-1], level)
                        
                        if breaklevel(self.data.Open[-1], self.data.Close[-1], level) == 1 or 2:
                            
                            breakinstances.append(Levelbreak(self.data.Date[-1], self.data.Time[-1], levelname, level, result, self.data.Open[-1], self.data.Close[-1], self.data.Volume[-1]))
                            self.breaklist.append([self.data.Date[-1], self.data.Time[-1], levelname, level, result, self.data.Open[-1], self.data.Close[-1], self.data.Volume[-1]])
                    
                    for x in self.breaklist:

                        if x[2] == 'idr_high':
                            self.idr_high_broken = True
                        if x[2] == 'idr_low':
                            self.idr_low_broken = True
                        if x[2] == 'dr_high':
                            self.dr_high_broken = True
                        if x[2] == 'dr_low':
                            self.dr_low_broken = True
                            
                if (self.data.Time[-1] == sessions['session_validity']):

                    #check if DR Concepts Rule is true or broken
                    if self.ec:  # early confirmation
                        if self.idr_high_broken and not self.dr_low_broken:
                            self.ec = False
                        if self.idr_low_broken and not self.dr_high_broken:
                            self.ec = False
                    if self.rule:  # rule
                        if self.dr_high_broken and not self.dr_low_broken:
                            self.rule = False
                        if self.dr_low_broken and not self.dr_high_broken:
                            self.rule = False
                    
                    sessioninstances.append(Session(sessions['session_name'], self.data.Date[-1], sessions['defining_hour_start'], sessions['defining_hour_end'], sessions['session_validity'], self.drhigh, self.drhightimestamp, self.drlow, self.drlowtimestamp, self.idrhigh, self.idrhightimestamp, self.idrlow, self.idrlowtimestamp, self.dr_mid, self.ec, self.rule))
                    
                    self.breaklist = []
                    self.breakinstances = []
                    self.drhourflag = False
                    self.drlow = ''
                    self.drhigh = ''
                    self.idrlow = ''
                    self.idrhigh = ''
                    self.drlowtimestamp = ''
                    self.drhightimestamp = ''
                    self.idrlowtimestamp = ''
                    self.idrhightimestamp = ''

                    self.idr_high_broken = False
                    self.idr_low_broken = False
                    self.dr_high_broken = False
                    self.dr_low_broken = False
                    self.ec = True
                    self.rule = True

# Create a Backtest object using the data and the strategy
bt = Backtest(data, DR_Backtesting, cash=1, commission=.000)
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