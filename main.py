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
        wait = WebDriverWait(driver, 15)
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            button.click()
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
            print(f"{url} — Woken successfully ✅")
        except TimeoutException:
            print(f"{url} — No wake-up button found, already awake ✅")
    except Exception as e:
        print(f"Error with {url}: {e}")
    finally:
        driver.quit()

for app in APP_URLS:
    wake_app(app)
