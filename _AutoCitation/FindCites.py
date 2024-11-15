"""
Uses google custom search api to optimize the speed of the program. The disadvantage of this alternative is that there is a limit of 100 request made per day or else you will have to pay.
"""

import os
import sys
import logging
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import re

# Configuration
LOG_DIR = "./log"
WEBSITES_LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 12
QUERY_FILE = os.path.join(LOG_DIR, 'search_queries.txt')
OUTPUT_FILE = os.path.join(LOG_DIR, "_websites_.json")

# Setup logging
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"Search_log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Check for missing environment variables
if not API_KEY or not SEARCH_ENGINE_ID:
    logging.error("API_KEY or SEARCH_ENGINE_ID is not set in environment variables.")
    sys.exit("Missing Google API key or Search Engine ID.")

def search_websites(query):
    """Search Google for websites related to the query and return the links."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        search_results = response.json().get('items', [])
        websites = [result['link'] for result in search_results] if search_results else ["No results found."]
        logging.info(f"Websites found for query '{query}': {websites}")
        return websites
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error for query '{query}': {e}")
        return [f"Network error: {e}"]
    except Exception as e:
        logging.error(f"An error occurred for query '{query}': {e}")
        return [f"Error: {e}"]

def create_input_file(websites, filename):
    """Create a JSON file with the retrieved websites."""
    try:
        with open(filename, "w") as f:
            json.dump({"websites": websites}, f, indent=4)
        logging.info(f"Input file '{filename}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating input file '{filename}': {e}")

def clean_query(query):
    """Clean the query by removing leading numbers and quotation marks."""
    return re.sub(r'^\d+\.\s*|"|"$', '', query).strip()

# Main script execution
try:
    with open(QUERY_FILE, 'r') as file:
        queries = [clean_query(line) for line in file if line.strip()]
    all_websites = []
    for query in queries:
        all_websites += search_websites(query)
    unique_websites = list(set(all_websites))[:WEBSITES_LIMIT]
    create_input_file(unique_websites, OUTPUT_FILE)
    with open('./_AutoCitation/log/process.log', 'a') as log_file:
        log_file.write("\n4")
except Exception as e:
    logging.error(f"Error in main execution: {e}")
