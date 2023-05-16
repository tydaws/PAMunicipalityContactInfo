import requests
from bs4 import BeautifulSoup
import urllib.parse
from fake_headers import Headers
import csv
import os
import re

header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=False  # generate misc headers
    )

def get_full_url(base, url):
    return urllib.parse.urljoin(base, url)

def find_contact_pages(url):
    try:
        resp = requests.get(url, headers=header.generate())
    except:
        return [url]
    soup = BeautifulSoup(resp.text, 'html.parser')

    baseUrl = re.search('.(.*).com', url)

    keywords = ['contact', 'directory', 'officer', 'information', 'personnel', 'staff']
    contact_pages = []
    for link in soup.find_all('a'):
        for key in keywords:
            if key in link.text.lower():
                contact_pages.append(get_full_url(url, link.get('href')))

    return contact_pages

def scrape_and_save(contact_pages, filename):

    textCollection = ''

    for url in contact_pages:
        try:
            resp = requests.get(url, headers=header.generate())
        except:
            print(f'Failed request for {url}')
            continue
        print(f'sending request for {url}')
        soup = BeautifulSoup(resp.text, 'html.parser')
        textCollection += soup.get_text()

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(textCollection)

def get_page(row):

    website = row[3]  # change to the website you want to scrape
    contact_pages = find_contact_pages(website)
    contact_pages.append(website)

    uniquePages = set(contact_pages)

    contact_pages = list(uniquePages)

    if contact_pages:
        print("Potential contact pages found:")
        for i, page in enumerate(contact_pages):
            print(f"{i+1}. {page}")

        scrape_and_save(contact_pages, f'{row[0]}-{row[1]}.txt')

        ##choice = int(input("Enter the number of the page you want to save: ")) - 1
        ##if 0 <= choice < len(contact_pages):
        ##    scrape_and_save(contact_pages[choice], 'contact_page.txt')
        ##else:
        ##    print("Invalid choice.")
    else:
        print('No potential contact pages found.')

def main():
    csv_file = 'url_list2.csv'

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        os.chdir(f'{os.getcwd()}/data')

        for i in range(1, len(rows)):
            get_page(rows[i])

if __name__ == '__main__':
    main()
