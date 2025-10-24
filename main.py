from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

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
            # Try simpler: find all buttons and click the right one by text
            buttons = wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
            )
            found = False
            for button in buttons:
                if "wake this app back up" in button.text.lower() or "get this app back up" in button.text.lower():
                    button.click()
                    found = True
                    print(f"Clicked wake button for {url}")
                    break
            if found:
                print(f"{url} — Woken successfully ✅")
            else:
                print(f"{url} — Wake button not found, app may be already awake or button unrecognized ❗")
        except TimeoutException:
            print(f"{url} — No buttons found (timeout), already awake or page load issue ❗")
    except Exception as e:
        print(f"Error with {url}: {e}")
    finally:
        driver.quit()

for app in APP_URLS:
    wake_app(app)
