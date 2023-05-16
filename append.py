import csv

def append_to_column(csv_file, column_index, output_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        for row in rows:
            if column_index < len(row):
                #row[column_index] += f" {row[0]} County Pennsylvania"
                row[column_index] += f" Pennsylvania"
        
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerows(rows)
            
        print(f"Appended first column value to column {column_index} and saved to {output_file}")

# Usage example
csv_file = 'municipalities.csv'  # Path to the input CSV file
column_index = 1  # Index of the column to append the value (zero-based index)
output_file = 'append.csv'  # Path to the output CSV file

append_to_column(csv_file, column_index, output_file)