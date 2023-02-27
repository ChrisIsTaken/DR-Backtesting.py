import csv

#Define variables to store counts of True and False values for each line type
adr_true_count = 0
adr_false_count = 0
odr_true_count = 0
odr_false_count = 0
rdr_true_count = 0
rdr_false_count = 0

#Open the CSV file
with open('sessions.csv') as csvfile:
    reader = csv.reader(csvfile)

    #Loop through each row in the CSV file
    for row in reader:
        # Check the line type
        if row[0] == 'ADR':
            # Increment the count of True or False values
            if row[-2] == 'True':
                adr_true_count += 1
            else:
                adr_false_count += 1
        elif row[0] == 'ODR':
            #Increment the count of True or False values
            if row[-2] == 'True':
                odr_true_count += 1
            else:
                odr_false_count += 1
        elif row[0] == 'RDR':
            #Increment the count of True or False values
            if row[-2] == 'True':
                rdr_true_count += 1
            else:
                rdr_false_count += 1

#Calculate the percentage of True and False values for each line type
adr_true_percent = adr_true_count / (adr_true_count + adr_false_count) * 100
adr_false_percent = adr_false_count / (adr_true_count + adr_false_count) * 100
odr_true_percent = odr_true_count / (odr_true_count + odr_false_count) * 100
odr_false_percent = odr_false_count / (odr_true_count + odr_false_count) * 100
rdr_true_percent = rdr_true_count / (rdr_true_count + rdr_false_count) * 100
rdr_false_percent = rdr_false_count / (rdr_true_count + rdr_false_count) * 100

# Print the results
print(f'ADR True percentage: {adr_true_percent:.2f}%')
print(f'ADR False percentage: {adr_false_percent:.2f}%')
print(f'ODR True percentage: {odr_true_percent:.2f}%')
print(f'ODR False percentage: {odr_false_percent:.2f}%')
print(f'RDR True percentage: {rdr_true_percent:.2f}%')
print(f'RDR False percentage: {rdr_false_percent:.2f}%')
