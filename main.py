from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

APP_URLS = [
    "https://askdata-rag-llm.streamlit.app/",
    "https://order-inbox.streamlit.app/"
]

def wake_app(url):
    print(f"Visiting {url}")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 60)
        try:
            # Find all buttons, click the one containing 'get this app back up'
            buttons = wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
            )
            found = False
            for button in buttons:
                if "get this app back up" in button.text.lower():
                    button.click()
                    found = True
                    print(f"Clicked wake button for {url}")
                    break
            time.sleep(5)  # Wait for wake-up action to process

            # Take a screenshot
            driver.save_screenshot("after_click.png")
            print(f"Screenshot taken for {url} after wake attempt.")

            # Wait for an app element to verify the app woke up (e.g., Streamlit sidebar)
            try:
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSidebar']"))
                )
                print(f"{url} — App sidebar detected, app woke successfully ✅")
            except TimeoutException:
                print(f"{url} — App sidebar NOT detected, app may NOT be awake ❗")
        except TimeoutException:
            print(f"{url} — No wake-up button found (timeout or already awake) ❗")
    except Exception as e:
        print(f"Error with {url}: {e}")
    finally:
        driver.quit()

for app in APP_URLS:
    wake_app(app)
