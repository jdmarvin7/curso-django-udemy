import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

# --headless
def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS'):
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('https://www.udemy.com/')
    sleep(5)
    browser.quit()