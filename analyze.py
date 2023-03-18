import csv

no_early_indication_count = 0
rdr_no_early_indication_count = 0
adr_no_early_indication_count = 0
odr_no_early_indication_count = 0
early_indication_bearish_broken = 0
rdr_early_indication_bearish_broken = 0
adr_early_indication_bearish_broken = 0
odr_early_indication_bearish_broken = 0
early_indication_bullish_broken = 0
rdr_early_indication_bullish_broken = 0
adr_early_indication_bullish_broken = 0
odr_early_indication_bullish_broken = 0
early_indication_bearish_held = 0
rdr_early_indication_bearish_held = 0
adr_early_indication_bearish_held = 0
odr_early_indication_bearish_held = 0
early_indication_bullish_held = 0
rdr_early_indication_bullish_held = 0
adr_early_indication_bullish_held = 0
odr_early_indication_bullish_held = 0
no_confirmation_count = 0
rdr_no_confirmation_count = 0
adr_no_confirmation_count = 0
odr_no_confirmation_count = 0
confirmation_bearish_broken = 0
rdr_confirmation_bearish_broken = 0
adr_confirmation_bearish_broken = 0
odr_confirmation_bearish_broken = 0
confirmation_bullish_broken = 0
rdr_confirmation_bullish_broken = 0
adr_confirmation_bullish_broken = 0
odr_confirmation_bullish_broken = 0
confirmation_bearish_held = 0
rdr_confirmation_bearish_held = 0
adr_confirmation_bearish_held = 0
odr_confirmation_bearish_held = 0
confirmation_bullish_held = 0
rdr_confirmation_bullish_held = 0
adr_confirmation_bullish_held = 0
odr_confirmation_bullish_held = 0

# Open the CSV file
with open('sessions.csv', 'r') as sessions, open('breaks_candle.csv', 'r') as candlebreaks, open('breaks_wick.csv', 'r') as wickbreaks, open(r"data\USATECHIDXUSD.csv") as pricedata:
    readersession = csv.reader(sessions)
    readercandlebreaks = csv.reader(candlebreaks)
    readerwickbreaks = csv.reader(wickbreaks)
    readerprice = csv.reader(pricedata)
    
    #Iterate through each row in the CSV file
    for row in readersession:

        #Count for early indication
        if row[-2] == '0':

            no_early_indication_count += 1

            if row[0] == 'RDR':
                rdr_no_early_indication_count += 1
            elif row[0] == 'ADR':
                adr_no_early_indication_count += 1
            elif row[0] == 'ODR':
                odr_no_early_indication_count += 1
        
        if row[-2] == '1':
            early_indication_bearish_broken += 1

            if row[0] == 'RDR':
                rdr_early_indication_bearish_broken += 1
            elif row[0] == 'ADR':
                adr_early_indication_bearish_broken += 1
            elif row[0] == 'ODR':
                odr_early_indication_bearish_broken += 1

        if row[-2] == '2':
            early_indication_bullish_broken += 1

            if row[0] == 'RDR':
                rdr_early_indication_bullish_broken += 1
            elif row[0] == 'ADR':
                adr_early_indication_bullish_broken += 1
            elif row[0] == 'ODR':
                odr_early_indication_bullish_broken += 1

        if row[-2] == '3':
            early_indication_bearish_held += 1

            if row[0] == 'RDR':
                rdr_early_indication_bearish_held += 1
            elif row[0] == 'ADR':
                adr_early_indication_bearish_held += 1
            elif row[0] == 'ODR':
                odr_early_indication_bearish_held += 1

        if row[-2] == '4':
            early_indication_bullish_held += 1

            if row[0] == 'RDR':
                rdr_early_indication_bullish_held += 1
            elif row[0] == 'ADR':
                adr_early_indication_bullish_held += 1
            elif row[0] == 'ODR':
                odr_early_indication_bullish_held += 1

        #Count for confirmation
        if row[-1] == '0':

            no_confirmation_count += 1

            if row[0] == 'RDR':
                rdr_no_confirmation_count += 1
            elif row[0] == 'ADR':
                adr_no_confirmation_count += 1
            elif row[0] == 'ODR':
                odr_no_confirmation_count += 1
        
        if row[-1] == '1':
            confirmation_bearish_broken += 1

            if row[0] == 'RDR':
                rdr_confirmation_bearish_broken += 1
            elif row[0] == 'ADR':
                adr_confirmation_bearish_broken += 1
            elif row[0] == 'ODR':
                odr_confirmation_bearish_broken += 1

        if row[-1] == '2':
            confirmation_bullish_broken += 1

            if row[0] == 'RDR':
                rdr_confirmation_bullish_broken += 1
            elif row[0] == 'ADR':
                adr_confirmation_bullish_broken += 1
            elif row[0] == 'ODR':
                odr_confirmation_bullish_broken += 1

        if row[-1] == '3':
            confirmation_bearish_held += 1

            if row[0] == 'RDR':
                rdr_confirmation_bearish_held += 1
            elif row[0] == 'ADR':
                adr_confirmation_bearish_held += 1
            elif row[0] == 'ODR':
                odr_confirmation_bearish_held += 1

        if row[-1] == '4':
            confirmation_bullish_held += 1

            if row[0] == 'RDR':
                rdr_confirmation_bullish_held += 1
            elif row[0] == 'ADR':
                adr_confirmation_bullish_held += 1
            elif row[0] == 'ODR':
                odr_confirmation_bullish_held += 1


# Calculate and output the percentages

# Probability that early indication held
print("Probability for early indication holding true overall:")
early_indication_held_count = early_indication_bearish_held + early_indication_bullish_held
early_indication_held_percentage = (early_indication_held_count / (early_indication_bearish_broken + early_indication_bullish_broken + early_indication_held_count)) * 100
print(f"    Probability that early indication held: {early_indication_held_percentage:.2f}%")
print("")

# Probability that confirmation held
print("Probability for confirmation holding true overall.")
confirmation_held_count = confirmation_bearish_held + confirmation_bullish_held
confirmation_held_percentage = (confirmation_held_count / (confirmation_bearish_broken + confirmation_bullish_broken + confirmation_held_count)) * 100
print(f"    Probability that confirmation held: {confirmation_held_percentage:.2f}%")
print("")

# Probability that early indication held for each of the sessions
print("Probability of early indication holding true for each session:")
rdr_early_indication_held_percentage = (rdr_early_indication_bearish_held + rdr_early_indication_bullish_held) / (rdr_early_indication_bearish_broken + rdr_early_indication_bullish_broken + (rdr_early_indication_bearish_held + rdr_early_indication_bullish_held)) * 100
adr_early_indication_held_percentage = (adr_early_indication_bearish_held + adr_early_indication_bullish_held) / (adr_early_indication_bearish_broken + adr_early_indication_bullish_broken + (adr_early_indication_bearish_held + adr_early_indication_bullish_held)) * 100
odr_early_indication_held_percentage = (odr_early_indication_bearish_held + odr_early_indication_bullish_held) / (odr_early_indication_bearish_broken + odr_early_indication_bullish_broken + (odr_early_indication_bearish_held + odr_early_indication_bullish_held)) * 100
print(f"    Probability that early indication held for RDR: {rdr_early_indication_held_percentage:.2f}%")
print(f"    Probability that early indication held for ADR: {adr_early_indication_held_percentage:.2f}%")
print(f"    Probability that early indication held for ODR: {odr_early_indication_held_percentage:.2f}%")
print("")

# Probability that confirmation held for each of the sessions
print("Probability of confirmation holding true for each session:")
rdr_confirmation_held_percentage = (rdr_confirmation_bearish_held + rdr_confirmation_bullish_held) / (rdr_confirmation_bearish_broken + rdr_confirmation_bullish_broken + (rdr_confirmation_bearish_held + rdr_confirmation_bullish_held)) * 100
adr_confirmation_held_percentage = (adr_confirmation_bearish_held + adr_confirmation_bullish_held) / (adr_confirmation_bearish_broken + adr_confirmation_bullish_broken + (adr_confirmation_bearish_held + adr_confirmation_bullish_held)) * 100
odr_confirmation_held_percentage = (odr_confirmation_bearish_held + odr_confirmation_bullish_held) / (odr_confirmation_bearish_broken + odr_confirmation_bullish_broken + (odr_confirmation_bearish_held + odr_confirmation_bullish_held)) * 100
print(f"    Probability that confirmation held for RDR: {rdr_confirmation_held_percentage:.2f}%")
print(f"    Probability that confirmation held for ADR: {adr_confirmation_held_percentage:.2f}%")
print(f"    Probability that confirmation held for ODR: {odr_confirmation_held_percentage:.2f}%")