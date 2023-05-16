import re
import string
import os
import csv

def remove_duplicates(file_path):
    
    os.chdir(f'{os.getcwd()}/data')

    # Read the input file and store the lines in a list
    cleanLines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()


    # Remove duplicates by converting the list to a set and back to a list
    unique_lines = list(set(lines))

    current_directory = os.getcwd() 
    parent_directory = os.path.dirname(current_directory)
    os.chdir(parent_directory)
    os.chdir(f'{os.getcwd()}/clean')

    # Write the modified content to the output file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

    print("Duplicates removed successfully. Result saved to", file_path)

    current_directory = os.getcwd() 
    parent_directory = os.path.dirname(current_directory)
    os.chdir(parent_directory)


# Example usage
input_file_path = 'input.txt'    # Replace with the path to the input file
output_file_path = 'output.txt'  # Replace with the desired path for the output file

with open('url_list.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    text = list(reader)
for row in text:
    if row[0] == 'COUNTY':
        continue
    county = row[0]
    municipality = row[1]
    file_path = f'{county}-{municipality}.txt'
    remove_duplicates(file_path)