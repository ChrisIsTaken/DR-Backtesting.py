import csv

# Open the CSV file
with open('sessions.csv', 'r') as sessions, open('breaks.csv', 'r') as breaks, open(r"data\USATECHIDXUSD.csv") as pricedata:
    readersession = csv.reader(sessions)
    readerbreaks = csv.reader(breaks)
    readerprice = csv.reader(pricedata)

    #check for ec
    for row in readersession:
        row[4] 
        if row[-2] == 3:
            