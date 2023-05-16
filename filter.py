import csv

def filter_csv(input_file, output_file):
    with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
        reader = csv.reader(csv_input)
        writer = csv.writer(csv_output)
        
        for row in reader:
            if len(row) >= 3 and row[2] != "Borough":
                writer.writerow(row)

# Example usage
input_file = 'append.csv'  # Replace with your input CSV file path
output_file = 'filter.csv'  # Replace with your output CSV file path

filter_csv(input_file, output_file)