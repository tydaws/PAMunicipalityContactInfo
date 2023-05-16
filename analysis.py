import openai
import os
import csv
import time

# Set up your OpenAI API credentials
openai.api_key = 'ENTERKEYHERE'

document = ''

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to generate text using GPT-3.5 Turbo
def generate_text(prompt):
    failed = True
    while failed == True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}],
                temperature=0.7,
                max_tokens=768,  # Adjust the desired length of the generated text
                n = 1,           # Generate a single response
                stop=None       # Let the model generate as much text as it wants
            )
        except Exception as inst:
            print('Request to OpenAI Failed. Trying again.')
            print(inst)
            time.sleep(10)
            if 'reduce the length' in str(inst).lower():
                return 'ERROR 404: NO INFORMATION FOUND'
        else:
            return response.choices[0]['message']['content']

# Breaks text into chunks if larger than gpt-3.5-turbo request (token) limit
def break_text(text):
    chunks = []
    max_chunk_size = 12000
    if len(text) > max_chunk_size:
        for i in range(0, len(text), max_chunk_size):
            chunks.append(text[i:i+max_chunk_size])
    else:
        chunks.append(text)
    return chunks

def run_analysis(file_path, county, municipality):
    promptCollection = []

    prompt = f"Your job is to parse website text. You are looking for any and all contact information for officials, staff and administration for {municipality} in {county} County. Provide ALL phone numbers, addresses and email addresses that you find, but only if the information is RELEVANT to the stated prompt.  If you are unable to find any relevant information, or if the information is for the wrong township/city etc, respond with  \"ERROR 404: NO INFORMATION FOUND\". The website text is shown below:"
    # Read text from file
    text = read_text_from_file(file_path)
    chunks = break_text(text)
    chunkCount = 1
    for chunk in chunks:
        chunkPrompt = prompt + chunk
        generated_text = generate_text(chunkPrompt)
        promptCollection.append([f'AI Attempt #{chunkCount}: \n\n', f'{generated_text}\n\n\n'])
        chunkCount+= 1
    return promptCollection

def county_analysis(countyMunicipalities):
    county_results = []
    for row in countyMunicipalities:
        county = row[0]
        municipality = row[1]
        url = row[3]
        file_path = f'{county}-{municipality}.txt'
        result = run_analysis(file_path, county, municipality)
        county_results.append([municipality, url, result])
    return county_results
        

def report_staging(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        cleanRows = []
        for i in range(1, len(rows)):
            cleanRows.append(rows[i])
            
        county_list = get_unique_values_in_column(cleanRows, 0)
        county_list = sorted(county_list)
        os.chdir(f'{os.getcwd()}/data')
        for county in county_list:
            build_county_header(county)
            countyMunicipalities = get_rows_for_county(cleanRows, county)
            results = county_analysis(countyMunicipalities)
            countyData = build_county_results(results)
            print(f'Writing {county} County Data.')
            write_data(countyData)


def get_rows_for_county(rows, county):
    return [row for row in rows if row[0] == county]

def get_unique_values_in_column(array, column_index):
    unique_values = set()
    
    for row in array:
        unique_values.add(row[column_index])
    
    return list(unique_values)

def write_data(data):
    global document
    document += data
    print(data)


def build_county_results(results):
    countyData = ''

    for municipality in results:
        countyData += f'\n\n#{municipality[0]}#' + '\n'
        countyData += f'Web Address Sourced: {municipality[1]}\n\n'
        for attempt in municipality[2]:
            countyData += attempt[0] + attempt[1]

    return countyData


def build_county_header(county):
    global document
    document += f'##{county} County##\n\n\n'
    print(f'Writing {county} County Header')

document += '###Pennsylvania Municipalities Contact Info### \n\n\n'


print("Writing main header.")

report_staging('url_list.csv')

current_directory = os.getcwd() 
parent_directory = os.path.dirname(current_directory)
os.chdir(parent_directory)

with open('out.txt', 'w', encoding='utf-8') as file:
        file.writelines(document)