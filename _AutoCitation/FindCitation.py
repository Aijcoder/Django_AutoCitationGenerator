"""
Uses mybib to find citations as my citation finding is not too good, it often can not find some information.
"""
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configuration
LOG_DIR = './log'
LOG_FILE_PATH = os.path.join(LOG_DIR, 'output.json')
JSON_FILE_PATH = os.path.join(LOG_DIR,'_websites_.json')
URL = "https://www.mybib.com/tools/mla-citation-generator"
CHROME_DRIVER_PATH = "./chromedriver"

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Load URLs from the JSON file
with open(JSON_FILE_PATH, 'r') as file:
    data = json.load(file)
    websites = data.get("websites", [])

# Initialize Chrome options
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")  # Uncomment if you want to run headless
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Set up the WebDriver service
service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# List to store citation results
citations = []

# Iterate over each website to generate citations
for geturl in websites:
    try:
        # Navigate to the MyBib website
        driver.get(URL)

        # Wait for the input field to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder='Enter or paste a web address to cite. URLs to PDFs are supported.']"))
        )

        # Find the input field and enter the URL
        citation_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='Enter or paste a web address to cite. URLs to PDFs are supported.']")
        citation_input.clear()
        citation_input.send_keys(geturl)
        citation_input.send_keys('\n')

        # Wait for the citation result to appear and click it
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.result button"))).click()

        # Wait for the citation output to be displayed
        citation_output = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='background: rgb(254, 241, 196); margin-bottom: 10px; padding: 20px;']"))
        )

        # Append the citation result to the citations list
        citations.append({"url": geturl, "citation": citation_output.text})
        print(f"Citation generated for {geturl}.")

    except TimeoutException:
        print(f"Timeout while processing {geturl}.")
    except NoSuchElementException as e:
        print(f"Element not found for {geturl}: {e}")
    except Exception as e:
        print(f"An error occurred for {geturl}: {e}")

# Save all citations to a JSON file
with open(LOG_FILE_PATH, 'w') as json_file:
    json.dump(citations, json_file, indent=4)
print(f"Citations saved to {LOG_FILE_PATH}.")

# Close the WebDriver at the end
driver.quit()
