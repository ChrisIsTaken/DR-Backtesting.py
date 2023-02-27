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
    counts = {
        'ADR': {'True': 0, 'False': 0},
        'ODR': {'True': 0, 'False': 0},
        'RDR': {'True': 0, 'False': 0}
        }

    for row in reader:
        # Get the line type and True/False value
        line_type = row[0]
        tf_value = row[-2]
    
        # Increment the count for the line type and True/False value
        counts[line_type][tf_value] += 1

for line_type in counts:
    true_count = counts[line_type]['True']
    false_count = counts[line_type]['False']
    total_count = true_count + false_count
    true_percent = true_count / total_count * 100
    false_percent = false_count / total_count * 100
    print(f'{line_type} True: {true_percent:.2f}% False: {false_percent:.2f}%')
