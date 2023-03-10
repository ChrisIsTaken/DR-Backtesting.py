import csv

# Define the input and output file paths
input_file_path = r"data\USATECHIDXUSD.csv"
output_file_path = r"data\datasample_15-23.csv"

# Define the prefixes of the lines you want to extract
prefixes = ['2015.', '2016.', '2017.', '2018.', '2019.', '2020.', '2021.', '2022.', '2023.'] 

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:

    # Create a CSV reader and writer
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Loop through each row in the input file
    for row in reader:

        # Check if the row starts with any of the desired prefixes
        if any(row[0].startswith(prefix) for prefix in prefixes):

            # Write the row to the output file
            writer.writerow(row)
