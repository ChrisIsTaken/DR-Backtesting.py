from time import time
import datetime
import pandas as pd
from backtesting import Strategy
from backtesting import Backtest
import csv

# Load data from CSV file into a DataFrame
#data = pd.read_csv("data.csv", parse_dates={'timestamp': ['Date', 'Time']}, names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])
data = pd.read_csv("data.csv", names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])

data['timestamp'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%Y.%m.%d %H:%M')
data['hour'] = data['timestamp'].dt.hour
data['minute'] = data['timestamp'].dt.minute

# Define your strategy
class MyStrategy(Strategy):
    def init(self):
        print("Reached init(self)")
        #RDR Vars
        self.rdr_session_vars = {
            'session_name': 'RDR',                          #Var to store the sessions name
            'defining_hour_start': datetime.datetime.strptime("09:30", "%H:%M").time(),    #Var to store time when session's defining hour starts
            'defining_hour_end': datetime.datetime.strptime("10:30", "%H:%M").time(),   #Var to store time when session's defining hour ends
            'session_validity': datetime.datetime.strptime("13:00", "%H:%M").time(),      #Var to store time when session is invalid
            'dr_high': None,                                #Var to store dr high
            'dr_high_timestamp': None,                      #dr high timestamp
            'dr_low': None,                                 #Var to store dr low
            'dr_low_timestamp': None,                       #dr low timestamp
            'idr_high': None,                               #Var to store idr high
            'idr_high_timestamp': None,             
            'idr_low': None,                                #Var to store idr low
            'idr_low_timestamp': None,              
            'levelbreaks': [],                              #Variable to store all the breaks of relevant levels
            }

        #ODR Vars
        self.odr_session_vars = {
            'session_name': 'ODR',
            'defining_hour_start': datetime.datetime.strptime("03:00", "%H:%M").time(),
            'defining_hour_end': datetime.datetime.strptime("04:30", "%H:%M").time(),
            'session_validity': datetime.datetime.strptime("02:00", "%H:%M").time(),
            'dr_high': None,
            'dr_high_timestamp': None,
            'dr_low': None,
            'dr_low_timestamp': None,
            'idr_high': None,
            'idr_high_timestamp': None,
            'idr_low': None,
            'idr_low_timestamp': None,
            'levelbreaks': [],
        }

        #ADR Vars
        self.adr_session_vars = {
            'session_name': 'ADR',
            'defining_hour_start': datetime.datetime.strptime("19:30", "%H:%M").time(),
            'defining_hour_end': datetime.datetime.strptime("20:30", "%H:%M").time(),
            'session_validity': datetime.datetime.strptime("08:00", "%H:%M").time(),
            'dr_high': None,
            'dr_high_timestamp': None,
            'dr_low': None,
            'dr_low_timestamp': None,
            'idr_high': None,
            'idr_high_timestamp': None,
            'idr_low': None,
            'idr_low_timestamp': None,
            'levelbreaks': [],
        }

        # open a csv file to store the results
        print("opening csv file")
        self.csvfile = open('session_results.csv', 'a', newline='') 
        print("creating instance of csvwriter")
        self.csvwriter = csv.writer(self.csvfile)
        print("writing header of scvfile")
        self.csvwriter.writerow(['session_name', 'dr_high', 'dr_high_timestamp', 'dr_low', 'dr_low_timestamp', 'idr_high', 'idr_high_timestamp', 'idr_low', 'idr_low_timestamp', 'levelbreaks'])

    def next(self):
        print("Reached next(self)")


        for sessions in [self.rdr_session_vars, self.odr_session_vars, self.adr_session_vars]:

            #defining time of last candle
            last_candle_time = datetime.datetime.strptime(self.data.Time[-1], "%H:%M").time()

            # Your strategy logic here
            #Checking if current time is in between defining hour
            print(sessions['session_name'])
            print(last_candle_time)
            print(sessions['defining_hour_start'])
            print(sessions['defining_hour_end'])
            if last_candle_time >= sessions['defining_hour_start'] and last_candle_time < sessions['defining_hour_end']:
                print("session's defining hour is ongoing")
                #Update levels
                print("updating levels:")
                if (sessions['dr_high'] == None) or (self.data.Close[-1] > sessions['dr_high']):
                    sessions['dr_high'] = self.data.Close[-1]

                if (sessions['dr_low'] == None) or (self.data.Close[-1] < sessions['dr_low']):
                    sessions['dr_low'] = self.data.Close[-1]

                if (sessions['idr_high'] == None) or (self.data.High[-1] > sessions['idr_high']):
                    sessions['idr_high'] = self.data.High[-1]

                if (sessions['idr_low'] == None) or (self.data.Low[-1] < sessions['idr_low']):
                    sessions['idr_low'] = self.data.Low[-1]


                print("Updated values: drhigh:", sessions['dr_high'], "drlow: ", sessions['dr_low'], "idrhigh: ", sessions['idr_high'], "idrlow: ", sessions['idr_low'])


            else:
                print("Sessions hour has passed")
                #Check if session is still valid
                if last_candle_time > sessions['defining_hour_end'] and last_candle_time <= sessions['session_validity']:
                    print("session is still valid")
                    
                    def breaklevel(open_price, close_price, level):
                        if (open_price < level) and  (level > close_price):
                            return 1
                        elif (open_price > level) and (level < close_price):
                            return 2

                    levels = [sessions['dr_low'], sessions['idr_low'], sessions['dr_high'], sessions['idr_high']]
                    open_price, close_price = self.data.Open[-1], self.data.Close[-1]
                    print("entering level loop")
                    for level in levels:
                        result = breaklevel(open_price, close_price, level)
                        print("current result is:", result)
                        if result == 1 or result == 2:
                            print("adding the following to levelbreaks: ", sessions['session_name'], last_candle_time, level, result, open_price, close_price)
                            sessions['levelbreaks'].append([sessions['session_name'], last_candle_time, level, result, open_price, close_price])
                else:
                    #session is not valid anymore, append values to csv
                    self.csvwriter.writerow([sessions['session_name'], sessions['dr_high'], sessions['dr_high_timestamp'], sessions['dr_low'], sessions['dr_low_timestamp'], sessions['idr_high'], sessions['idr_high_timestamp'], sessions['idr_low'], sessions['idr_low_timestamp'], sessions['levelbreaks']])
                    self.csvfile.flush()
        
# Create a Backtest object using the data and the strategy
bt = Backtest(data, MyStrategy, cash=100000, commission=.002)
stats = bt.run()
print(stats)
#bt.plot()
