import csv

# Initialize count variables for each line type and boolean value
adr_early_true_count = 0
adr_early_false_count = 0
adr_true_count = 0
adr_false_count = 0
odr_early_true_count = 0
odr_early_false_count = 0
odr_true_count = 0
odr_false_count = 0
rdr_early_true_count = 0
rdr_early_false_count = 0
rdr_true_count = 0
rdr_false_count = 0

# Open the CSV file
with open('sessions.csv', 'r') as file:
    reader = csv.reader(file)
    
    # Iterate through each row in the CSV file
    for row in reader:
        # Check the line type and boolean values
        if row[0] == 'ADR':
            if row[-2] == 'True':
                adr_early_true_count += 1
            else:
                adr_early_false_count += 1
            if row[-1] == 'True':
                adr_true_count += 1
            else:
                adr_false_count += 1
        elif row[0] == 'ODR':
            if row[-2] == 'True':
                odr_early_true_count += 1
            else:
                odr_early_false_count += 1
            if row[-1] == 'True':
                odr_true_count += 1
            else:
                odr_false_count += 1
        elif row[0] == 'RDR':
            if row[-2] == 'True':
                rdr_early_true_count += 1
            else:
                rdr_early_false_count += 1
            if row[-1] == 'True':
                rdr_true_count += 1
            else:
                rdr_false_count += 1

# Calculate and output the percentage for each line type and boolean value
adr_early_confirmation_percentage = adr_early_true_count / (adr_early_true_count + adr_early_false_count) * 100
adr_confirmation_percentage = adr_true_count / (adr_true_count + adr_false_count) * 100
print(f'ADR early_confirmation percentage: {adr_early_confirmation_percentage:.2f}%')
print(f'ADR confirmation percentage: {adr_confirmation_percentage:.2f}%')

odr_early_confirmation_percentage = odr_early_true_count / (odr_early_true_count + odr_early_false_count) * 100
odr_confirmation_percentage = odr_true_count / (odr_true_count + odr_false_count) * 100
print(f'ODR early_confirmation percentage: {odr_early_confirmation_percentage:.2f}%')
print(f'ODR confirmation percentage: {odr_confirmation_percentage:.2f}%')

rdr_early_confirmation_percentage = rdr_early_true_count / (rdr_early_true_count + rdr_early_false_count) * 100
rdr_confirmation_percentage = rdr_true_count / (rdr_true_count + rdr_false_count) * 100
print(f'RDR early_confirmation percentage: {rdr_early_confirmation_percentage:.2f}%')
print(f'RDR confirmation percentage: {rdr_confirmation_percentage:.2f}%')
