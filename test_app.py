from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess

# Start Streamlit app in background
proc = subprocess.Popen(["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"])
time.sleep(5)  # Wait for app to start

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://localhost:8501")

# Test addition
num1 = driver.find_element("xpath", "//input[@type='number'][1]")
num1.send_keys("5")
num2 = driver.find_element("xpath", "//input[@type='number'][2]")
num2.send_keys("3")
driver.find_element("xpath", "//div[@data-testid='stSelectbox']").click()
driver.find_element("xpath", "//p[text()='Add']").click()
driver.find_element("xpath", "//button[@kind='primary']").click()

time.sleep(2)
result = driver.find_element("xpath", "//section[@data-testid='stMarkdownContainer']").text
assert "Result: 8.0" in result

driver.quit()
proc.terminate()  # Stop app
print("Test passed!")
