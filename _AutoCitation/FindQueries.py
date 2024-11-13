"""
Uses julius.ai, it have no defence against bots and it is free, the only problem is that it has a character limit of 1200, I wish i will have better options.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Constants
LOG_DIR = './log'
LOG_FILE_PATH = os.path.join(LOG_DIR, 'output.log')
SEARCH_QUERIES_FILE_PATH = os.path.join(LOG_DIR,'search_queries.txt')
URL = "https://julius.ai/ai-chatbot"  # Adjust if necessary
CHROME_DRIVER_PATH = "./chromedriver"
LENGTH_LIMIT = 969

# Setup
os.makedirs(LOG_DIR, exist_ok=True)

# Get text to classify
text_to_classify = sys.argv[1] if len(sys.argv) > 1 else """
    In an age where climate change and environmental degradation are pressing concerns, the concept of sustainable living has gained significant traction. Sustainable living refers to a lifestyle that aims to reduce an individual's or society's use of the Earth's natural resources and personal resources. The goal is to create a balance between ecological health, economic viability, and social equity.
    One of the primary reasons sustainable living is crucial is the alarming rate at which we consume resources. According to the Global Footprint Network, humanity's demand for ecological resources exceeds what the Earth can regenerate in a year, leading to a deficit that can only worsen over time. By adopting sustainable practices, individuals can help to mitigate this imbalance.
"""

# Load stopwords
with open("resources/stopwords", 'r') as f:
    stopwords = set(f.read().splitlines())

# Filter input text
filtered_text = ' '.join(word for word in text_to_classify.split() if word.lower() not in stopwords).strip()
with open('./_AutoCitation/log/process.log', 'a') as log_file:
    log_file.write("Reading and filtering text - SUCCESS")
# Log filtered text
with open(LOG_FILE_PATH, 'a') as log_file:
    log_file.write("Filtered text: " + filtered_text + "\n")

if len(filtered_text) >= LENGTH_LIMIT:
    filtered_text = filtered_text[:LENGTH_LIMIT]


classification_prompt = (
    f"Given the following text, please classify it into one of the types: argumentative essay, "
    f"narrative essay, expository essay, news article, blog post, or other. Text: {filtered_text}"
)

# Chrome driver setup
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(executable_path=CHROME_DRIVER_PATH)

# Start WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get(URL)
    classification_result=''
    # Loop until a valid classification result is received or timeout occurs
    start_time = time.time()
    while True:
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flex.items-center.rounded-md.border.bg-transparent"))
        )
        
        message_box.send_keys(classification_prompt, Keys.RETURN)

        # Wait for classification result
        try:
            classification_result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.font-semibold.text-foreground"))
            ).text

            # Log the classification result
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write("Classification Result: " + classification_result + "\n")
            break
        except (NoSuchElementException, TimeoutException):
            if time.time() - start_time > 30:  # 30 seconds timeout
                raise TimeoutException("Timeout while waiting for classification result.")
            driver.get(URL)

    driver.refresh()
    with open('./_AutoCitation/log/process.log', 'a') as log_file:
        log_file.write("Classifying type of text - SUCCESS[" + classification_result + ']')
    # Generate Google search queries based on classification result
    search_query_prompt = (
        f"The text is: {filtered_text} And based on the classification result '{classification_result}', "
        "please generate a bold Google search query to find related articles, videos, or other resources. "
        "Generate 3 queries and end the response with 'END_OF_RES'."
    )
    message_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flex.items-center.rounded-md.border.bg-transparent"))
    )
    message_box.send_keys(search_query_prompt, Keys.RETURN)

    # Wait for search results
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"END_OF_RES")]'))
    )
    time.sleep(1)
    search_queries = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.font-semibold.text-foreground"))
    )
    
    # Log search queries and save to file
    with open(LOG_FILE_PATH, 'a') as log_file, open(SEARCH_QUERIES_FILE_PATH, 'w') as search_queries_file:
        for i, query_element in enumerate(search_queries, start=1):
            query = query_element.text
            log_file.write(f"Generated Google Search Query {i}: {query}\n")
            search_queries_file.write(query + "\n")
    with open('./_AutoCitation/log/process.log', 'a') as log_file:
        log_file.write("Generating queries - SUCCESS")
except (NoSuchElementException, TimeoutException) as e:
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f"Error occurred: {type(e).__name__}: {e}\n")

