"""
It always fails to find the authour or the publisher while also returning publish dates later than the current year 2024.
That's why i just used selenium on mybib.
"""

import requests
from bs4 import BeautifulSoup
import re

def generate_citation(title, authors, publisher, year, url):
    citation = f"{', '.join(authors)}. *{title}*. {publisher}, {year}, {url}."
    return citation

def get_webpage_info(url):
    try:
        response = requests.get(url,verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title else "Untitled"

        authors = []
        author_meta = soup.find_all('meta', attrs={'name': 'author'})
        for meta in author_meta:
            authors.append(meta.get('content').strip())
        
        if not authors:
            h1_tags = soup.find_all(['h1', 'h2'])
            for tag in h1_tags:
                if tag.string:
                    authors.append(tag.string.strip())
                    break
        
        publisher = url.split("//")[-1].split("/")[0]

        date_meta = soup.find('meta', attrs={'name': 'date'}) or soup.find('meta', attrs={'property': 'article:published_time'})
        if date_meta:
            year = date_meta.get('content').strip()
            year = re.search(r'\d{4}', year).group(0) if re.search(r'\d{4}', year) else "n.d."
        else:
            year = "n.d."

        return title, authors, publisher, year
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None, [], None, None

def main():
    print("Welcome to EasyBib Simulation (MLA 9 Format - Detailed Citation)!")
    
    url = input("Enter the website URL: ")

    title, authors, publisher, year = get_webpage_info(url)

    if title and publisher:
        citation = generate_citation(title, authors, publisher, year, url)
        print("\nGenerated Citation (MLA 9 Format):")
        print(citation)
    else:
        print("Failed to generate citation due to invalid URL or missing information.")

if __name__ == "__main__":
    main()
