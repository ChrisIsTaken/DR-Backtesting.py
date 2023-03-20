import csv

class LevelBreaksAnalyzer:
    def __init__(self, sessions_csv_path, breaks_csv_path):
        self.rdr_session = {
            'session_name': 'RDR',                          #Var to store the sessions name
            'defining_hour_start': "09:30",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "10:25",                   #Var to store time when session's defining hour ends
            'session_validity_start': "10:30",
            'session_validity_end': "16:00",                    #Var to store time when session is invalid
        }

        self.adr_session = {
            'session_name': 'ADR',                          #Var to store the sessions name
            'defining_hour_start': "19:30",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "20:25",                   #Var to store time when session's defining hour ends
            'session_validity_start': "20:30",
            'session_validity_end': "02:00",                    #Var to store time when session is invalid
        }

        self.odr_session = {
            'session_name': 'ODR',                          #Var to store the sessions name
            'defining_hour_start': "03:00",                 #Var to store time when session's defining hour starts
            'defining_hour_end': "03:55",                   #Var to store time when session's defining hour ends
            'session_validity_start': "04:00",
            'session_validity_end': "08:30",                    #Var to store time when session is invalid
        }

        self.sessions = {
            self.rdr_session['session_name']: self.rdr_session,
            self.adr_session['session_name']: self.adr_session,
            self.odr_session['session_name']: self.odr_session,
        }

        self.breaks = {}
        self.load_sessions(sessions_csv_path)
        self.load_breaks(breaks_csv_path)
        self.analyze_breaks()

    def load_sessions(self, sessions_csv_path):
        with open(sessions_csv_path, 'r') as sessions_file:
            reader = csv.reader(sessions_file)
            for i, row in enumerate(reader):
                if i == 0:  # skip header row
                    continue
                session_name, defining_hour_start, defining_hour_end, session_validity_start, session_validity_end = row
                session = {
                    'session_name': session_name,
                    'defining_hour_start': defining_hour_start,
                    'defining_hour_end': defining_hour_end,
                    'session_validity_start': session_validity_start,
                    'session_validity_end': session_validity_end,
                }
                self.sessions[session_name] = session

    def load_breaks(self, breaks_csv_path):
        with open(breaks_csv_path, 'r') as breaks_file:
            reader = csv.reader(breaks_file)
            for i, row in enumerate(reader):
                if i == 0:  # skip header row
                    continue
                date, time, levelname, level, result_candle, open_price, close_price, volume = row
                break_item = {
                    'date': date,
                    'time': time,
                    'levelname': levelname,
                    'level': level,
                    'result_candle': result_candle,
                    'open_price': open_price,
                    'close_price': close_price,
                    'volume': volume,
                }
                if date not in self.breaks:
                    self.breaks[date] = []
                self.breaks[date].append(break_item)

    def analyze_breaks(self):
        for date, breaks in self.breaks.items():
            for session_name, session in self.sessions.items():
                defining_hour_start = session['defining_hour_start']
                defining_hour_end = session['defining_hour_end']
                session_validity_start = session['session_validity_start']
                session_validity_end = session['session_validity_end']
                relevant_breaks = []
                for break_item in breaks:
                    break_time = break_item['time']
                    if self.is_valid_break_time(break_time, defining_hour_start, defining_hour_end, session_validity_start, session_validity_end):
                        relevant_breaks.append(break_item)
                if relevant_breaks:
                    self.print_breaks(session_name, date, relevant_breaks)

    def is_valid_break_time(self, break_time, defining_hour_start, defining_hour_end, session_validity_start, session_validity_end):
        if break_time < defining_hour_start or break_time > defining_hour_end:
            return False
        if break_time >= session_validity_start and break_time <= session_validity_end:
            return False
        return True

    def print_breaks(self, session_name, date, relevant_breaks):
        print(f"Session: {session_name}, Date: {date}")
        for break_item in relevant_breaks:
            levelname = break_item['levelname']
            level = break_item['level']
            result_candle = break_item['result_candle']
            open_price = break_item['open_price']
            close_price = break_item['close_price']
            volume = break_item['volume']
            print(f"Levelname: {levelname}, Level: {level}, Result Candle: {result_candle}, Open Price: {open_price}, Close Price: {close_price}, Volume: {volume}")

analyzer = LevelBreaksAnalyzer('sessions.csv', 'breaks.csv')
