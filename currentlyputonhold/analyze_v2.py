import csv

# Define dictionaries to store counts for each session
sessioninstances = {
    'ADR':
        {'early': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0},
         'confirmed': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0}},
    'ODR':
        {'early': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0},
         'confirmed': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0}},
    'RDR':
        {'early': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0},
         'confirmed': {'bearish_broke': 0, 'bullish_broke': 0, 'bearish_held': 0, 'bullish_held': 0, 'none': 0}}}

total_early_held = 0
total_confirmed_held = 0
total_early_broke = 0
total_confirmed_broke = 0

# Open the CSV file
with open('sessions.csv', 'r') as sessions_file:
    readersession = csv.reader(sessions_file)
    for row in readersession:
        # Extract the session and rule data from the current row
        session = row[0]
        early_indication = int(row[-2])
        confirmation = int(row[-1])
        
        # Update the counts based on the early indication
        if early_indication == 0:
            sessioninstances[session]['early']['none'] += 1
        elif early_indication == 1:
            sessioninstances[session]['early']['bearish_broke'] += 1
            total_early_broke += 1
        elif early_indication == 2:
            sessioninstances[session]['early']['bullish_broke'] += 1
            total_early_broke += 1
        elif early_indication == 3:
            sessioninstances[session]['early']['bearish_held'] += 1
            total_early_held += 1
        elif early_indication == 4:
            sessioninstances[session]['early']['bullish_held'] += 1
            total_early_held += 1
            
        # Update the counts based on the confirmation
        if confirmation == 0:
            sessioninstances[session]['confirmed']['none'] += 1
        elif confirmation == 1:
            sessioninstances[session]['confirmed']['bearish_broke'] += 1
            total_confirmed_broke += 1
        elif confirmation == 2:
            sessioninstances[session]['confirmed']['bullish_broke'] += 1
            total_confirmed_broke += 1
        elif confirmation == 3:
            sessioninstances[session]['confirmed']['bearish_held'] += 1
            total_confirmed_held += 1
        elif confirmation == 4:
            sessioninstances[session]['confirmed']['bullish_held'] += 1
            total_confirmed_held += 1

# Calculate and output the percentages for each category
for session, data in sessioninstances.items():
    print(f"Session {session}:")
    print("")

    early_numerator = data['early']['bearish_held'] + data['early']['bullish_held']
    early_denominator = early_numerator + data['early']['bearish_broke'] + data['early']['bullish_broke']
    early_percentage = (early_numerator / early_denominator) * 100
    print("Total early indications that held: ", early_percentage, "%")

    confi_numerator = data['confirmed']['bearish_held'] + data['confirmed']['bullish_held']
    confi_denominator = confi_numerator + data['confirmed']['bearish_broke'] + data['confirmed']['bullish_broke']
    confi_percentage = (confi_numerator / confi_denominator) * 100
    print("Total confirmations that held: ", confi_percentage, "%")

    print("")

    for category in ['bearish_broke', 'bullish_broke', 'bearish_held', 'bullish_held', 'none']:
        total = sum([data['early']['bearish_broke'], data['early']['bullish_broke'], data['early']['bearish_held'], 
                     data['early']['bullish_held'], data['early']['none'], data['confirmed']['bearish_broke'], 
                     data['confirmed']['bullish_broke'], data['confirmed']['bearish_held'], data['confirmed']['bullish_held'], 
                     data['confirmed']['none']])
        if total > 0:
            early_percent = (data['early'][category] / total) * 100
            confirmed_percent = (data['confirmed'][category] / total) * 100
            print(f"{category}: Early - {early_percent:.2f}%, Confirmed - {confirmed_percent:.2f}%")

    print("")
    print("----------------------------")
    print("")

# Output the overall percentages
print("Overall percentages:")
print("Total early indications that held: ", (total_early_held / (total_early_held + total_early_broke)) * 100, "%")
print("Total confirmations that held: ", (total_confirmed_held / (total_confirmed_held + total_confirmed_broke)) * 100, "%")