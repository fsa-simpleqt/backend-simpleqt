# import requests
# from bs4 import BeautifulSoup

# url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'  # Replace with the URL you intend to scrape
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Example of extracting all paragraph texts
# paragraphs = soup.find_all('p')
# for paragraph in paragraphs:
#     print(paragraph.text)


# # Extract all text from the body of the HTML document
# text = soup.body.get_text(separator=' ', strip=True)
# print(text)

#2

# import requests
# from bs4 import BeautifulSoup

# # List of URLs to scrape
# urls = [
#     'https://vietnix.vn/java-la-gi/', 'https://200lab.io/blog/python-la-gi/'
#     # Add more URLs as needed
# ]

# for url in urls:
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Extract and print all paragraph texts for each URL
#     paragraphs = soup.find_all('p')
#     print(f'Content from {url}:')
#     for paragraph in paragraphs:
#         print(paragraph.text)
#     print("\n")  # Print a new line for better readability between different URLs
    
#     # Extract all text from the body of the HTML document for each URL
#     text = soup.body.get_text(separator=' ', strip=True)
#     print(f'Full text from {url}:')
#     print(text)
#     print("="*100)  # Print a separator line for better readability between different URLs

# 4 add save file
# import requests
# from bs4 import BeautifulSoup
# import os

# # List of URLs to scrape
# urls = [
#     'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue',
#     # Add more URLs as needed
# ]

# for url in urls:
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Extracting base name of the URL to use as the filename
#     filename = os.path.basename(url).replace('%', '_').replace('?', '_') + '.txt'
    
#     # Open a new text file for writing the scraped data
#     with open(filename, 'w', encoding='utf-8') as file:
#         # Write the URL to the file
#         file.write(f'Content from {url}:\n')
        
#         # Extract and write all paragraph texts for each URL
#         paragraphs = soup.find_all('p')
#         for paragraph in paragraphs:
#             file.write(paragraph.text + '\n')
#         file.write("\n")  # Write a new line for better readability between different URLs
        
#         # Extract and write all text from the body of the HTML document for each URL
#         text = soup.body.get_text(separator=' ', strip=True)
#         file.write(f'Full text from {url}:\n')
#         file.write(text + '\n')
#         file.write("="*100 + '\n')  # Write a separator line for better readability between different URLs
    
#     # Print out a message to let you know the data has been written to the file
#     print(f'Scraped data from {url} has been saved to {filename}')

#5 It has internal link scrapping
# import requests
# from bs4 import BeautifulSoup
# import os

# # Initial list of main URLs to scan
# main_urls = [
#     'https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills',
#     # Add more main URLs as needed
# ]

# # Function to get all unique links from a given URL
# def get_all_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     links = soup.find_all('a')
#     unique_links = set()
#     for link in links:
#         href = link.get('href')
#         if href and href.startswith('/wiki/'):  # Filters out unwanted links and keeps wikipedia internal links
#             complete_link = f"https://en.wikipedia.org{href}"
#             unique_links.add(complete_link)
#     return list(unique_links)

# # Iterate over main URLs to get all specific links and scrape data from each
# for main_url in main_urls:
#     urls = get_all_links(main_url)  # Get all sub-links from the main URL
#     for url in urls:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Extracting base name of the URL to use as the filename
#         filename = os.path.basename(url).split('#')[0]  # Remove URL fragments
#         filename = filename.replace('%', '_').replace('?', '_') + '.txt'  # Replace special characters
        
#         # Open a new text file for writing the scraped data
#         with open(filename, 'w', encoding='utf-8') as file:
#             # Write the URL to the file
#             file.write(f'Content from {url}:\n\n')
            
#             # Extract and write all paragraph texts for each URL
#             paragraphs = soup.find_all('p')
#             for paragraph in paragraphs:
#                 file.write(paragraph.text + '\n\n')
#             file.write("="*100 + '\n')  # Write a separator line for better readability
        
#         # Print out a message to let you know the data has been written to the file
#         print(f'Scraped data from {url} has been saved to {filename}')

import requests
from bs4 import BeautifulSoup
import os

# Initial list of main URLs to scan
main_urls = [
    'https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills',
    # Add more main URLs as needed
]

# Function to get all unique links from a given URL
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    unique_links = set()
    for link in links:
        href = link.get('href')
        if href and not href.startswith('#') and not href.startswith('mailto:'):  # Filters out unwanted links like anchors and emails
            if not href.startswith('http'):  # Check if the link is relative
                href = url + href  # Construct the complete URL
            unique_links.add(href)
    return list(unique_links)

# Iterate over main URLs to get all specific links and scrape data from each
for main_url in main_urls:
    urls = get_all_links(main_url)  # Get all sub-links from the main URL
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracting base name of the URL to use as the filename
        filename = os.path.basename(url).split('#')[0]  # Remove URL fragments
        filename = filename.replace('%', '_').replace('?', '_') + '.txt'  # Replace special characters
        
        # Open a new text file for writing the scraped data
        with open(filename, 'w', encoding='utf-8') as file:
            # Write the URL to the file
            file.write(f'Content from {url}:\n\n')
            
            # Extract and write all paragraph texts for each URL
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                file.write(paragraph.text + '\n\n')
            file.write("="*100 + '\n')  # Write a separator line for better readability
        
        # Print out a message to let you know the data has been written to the file
        print(f'Scraped data from {url} has been saved to {filename}')

