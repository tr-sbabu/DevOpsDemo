from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

# Start Streamlit app in background
proc = subprocess.Popen(["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"])
time.sleep(5)  # Initial wait for app to start

# Set up headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Wait for page to load
driver.get("http://localhost:8501")
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

# Debug: Print page source
print("Page source:", driver.page_source[:500])  # Truncated for brevity

# Test addition
try:
    num1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='stNumberInput']")))
    num1.send_keys("5")
    num2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='stNumberInput']:nth-of-type(2)")))
    num2.send_keys("3")
    selectbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='stSelectbox']")))
    selectbox.click()
    add_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Add']")))
    add_option.click()
    calc_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[kind='primary']")))
    calc_button.click()

    # Wait for result
    result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='stMarkdownContainer']")))
    result_text = result.text
    print("Result text:", result_text)
    assert "Result: 8.0" in result_text, f"Expected 'Result: 8.0', got '{result_text}'"
    print("Test passed!")
except Exception as e:
    print("Test failed:", str(e))
finally:
    driver.quit()
    proc.terminate()
