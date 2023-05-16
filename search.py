import csv
import time
import json
import os 
import requests
from googlesearch import search
from duckduckgo_search import ddg

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
#subscription_key = os.environ['ee4108075d1a42a28b0ecec493041998']
endpoint = 'https://api.bing.microsoft.com/v7.0/search'

# Construct a request
mkt = 'en-US'
headers = { 'Ocp-Apim-Subscription-Key': 'ENTERKEYHERE' }

def is_bad_url(url):
    values = ['wikipedia.org', 'facebook.com', 'apps', 'google.com', 'bing.com', 'penndot.gov', 'wiki', 'mapquest', 'maps', 'livingplaces', 'leadertimes', 'triblive', '.pdf', 'zillow']

    for value in values:
        if value in url.lower():
            return True
    
    return False

def is_wikipedia_result(url):
    return 'wikipedia.org' in url.lower()

def is_facebook_result(url):
    return 'facebook.com' in url.lower()

def is_apps(url):
    return 'apps' in url.lower()

def get_non_sponsored_result(search_query):
    params = { 'q': search_query, 'mkt': mkt }
    results = requests.get(endpoint, headers=headers, params=params)
    page = results.json()['webPages']
    values = page['value']

    for value in values:
        if not value['url'].startswith("https://www.google.com/aclk") and not is_bad_url(value['url']):
            return value['url']

    return None

def search_non_sponsored_results(csv_file, query_column):
    non_sponsored_results = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = row[query_column]
            result = get_non_sponsored_result(query)
            if result:
                non_sponsored_results.append(result)
                print(f"Result: {result}")

    return non_sponsored_results

def append_array_to_csv(input_file, output_file, array):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    rows[0].append("URL")  # Append "URL" to the header row

    for i in range(1, len(rows)):
        rows[i].append(array[i - 1])

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"New CSV file '{output_file}' has been created with the appended column.")

# Example usage
csv_file = 'filter.csv'  # Path to your CSV file
output_file = 'url_list.csv' # output
query_column = 'MUNICIPALITY'  # Specify the column name containing the search queries

non_sponsored_results = search_non_sponsored_results(csv_file, query_column)

# Output to new CSV

append_array_to_csv(csv_file, output_file, non_sponsored_results)