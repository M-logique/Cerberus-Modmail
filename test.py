from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Set up Chrome driver
driver = webdriver.Firefox()  # Replace with your preferred browser

# Open the website
driver.get("https://coinmarketcap.com/currencies/notcoin/")

# Wait for the page to load
WebDriverWait(driver, 10)

# Take a screenshot
driver.save_screenshot("bybit_screenshot.png")

# Close the browser
driver.quit()