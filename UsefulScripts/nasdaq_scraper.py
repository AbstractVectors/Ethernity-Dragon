import time
import datetime
from datetime import timedelta
import json
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.nasdaq.com/market-activity/economic-calendar"
COOKIES = '//*[@id="onetrust-accept-btn-handler"]'
SCROLL_DATE_BAR = "/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]/button[1]"
SELECT_DATE = "/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/button"
ENTER_DATE = "/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/input"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")
#/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]/div/button[1]
# MAIN FUNCTION
def scrapema():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(URL)
    date = datetime.datetime(2022, 11, 10)
    print(date)
    driver.find_element(By.XPATH, COOKIES).click()
    driver.find_element(By.XPATH, SELECT_DATE).click()
    driver.find_element(By.XPATH, ENTER_DATE).clear()
    driver.find_element(By.XPATH, ENTER_DATE).send_keys("{}/{}/{}".format(date.month, date.day, date.year))
    terminate = datetime.datetime(2015, 6, 1)
    while (date >= terminate):
        try:
            page = driver.page_source
        except:
            pass
        else:
            try:
                soup = BeautifulSoup(page, "html.parser")
            except:
                pass
            else:
                scrape_date = soup.find("button", {"class": "time-belt__item time-belt__item--active"})
                print(scrape_date)
                events = soup.find_all("tr", {"class": "market-calendar-table__row"})
                for event in events:
                    scrape_date = scrape_date
                    #getData(event)
        yesterday = "/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]/div/button[3]"
        try:
            driver.find_element(By.XPATH, yesterday).click()
        except Exception as e:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        else:
            try:
                driver.find_element(By.XPATH, SCROLL_DATE_BAR).click()
            except Exception as e:
                print(e)
        date = date - timedelta(days=1)

scrapema()