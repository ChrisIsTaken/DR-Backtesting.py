import csv

# Define the input and output file paths
input_file_path = r"data\USATECHIDXUSD.csv"
output_file_path = r"data\datasample.csv"

# Define the prefix of the lines you want to extract
prefix = '2022.'

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:

    # Create a CSV reader and writer
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Loop through each row in the input file
    for row in reader:

        # Check if the row starts with the desired prefix
        if row[0].startswith(prefix):

            # Write the row to the output file
            writer.writerow(row)
