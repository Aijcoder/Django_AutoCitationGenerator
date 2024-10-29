"""
The main fail reason for this one is because of the cookie accept button since it never finds it, that is why I looked for the websites without cookit congiguration.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configuration
url = "https://julius.ai/ai-chatbot"  # Adjust if necessary
text_to_classify = "Your text here."  # Replace with the text you want to classify

# Initialize Chrome options
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Set up the Service with the path to your ChromeDriver
chrome_driver_path = "./chromedriver"
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver with Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the website
    driver.get(url)

    # Wait for and accept the cookie policy using the updated selector
    cookie_button_selector = 'button.message-button[aria-label="Accept"]'

    # Wait for the button to be clickable and click it
    cookie_button = WebDriverWait(driver, 1000000000).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_button_selector))
    )
    
    # Use ActionChains to ensure it's clickable
    cookie_button.click()
    
    # Optional: Add a brief sleep to allow any transitions to complete
    WebDriverWait(driver, 2)  # Optional wait time for transition

    # Wait for the message box to be present
    message_box_selector = 'textarea.chatbox'  # Selector for the message box
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, message_box_selector))
    )

    # Prepare the search prompt
    search_prompt = (
        "Given the following text, please classify it into one of the types: "
        "argumentative essay, narrative essay, expository essay, news article, blog post, or other.\n\n"
        f"Text: {text_to_classify}"
    )

    # Locate the message box and send the prompt
    message_box = driver.find_element(By.CSS_SELECTOR, message_box_selector)
    message_box.click()  # Focus on the message box
    message_box.clear()   # Clear the message box if necessary
    message_box.send_keys(search_prompt)
    message_box.send_keys(Keys.RETURN)

    # Wait for the results to load (adjust the selector based on where results appear)
    output_box_selector = "div.outputBox"  # Selector for the output box
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, output_box_selector))
    )

    # Get the output
    output_element = driver.find_element(By.CSS_SELECTOR, output_box_selector)
    output = output_element.text
    print(output)

except (NoSuchElementException, TimeoutException) as e:
    print(f"An error occurred: {e}")

