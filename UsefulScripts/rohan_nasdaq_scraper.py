import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time_utils import *

URL = "https://www.nasdaq.com/market-activity/economic-calendar"
SCROLL_DATE_BAR = "/html/body/div[2]/div/main/div[2]/div[2]/div/div/div[2]/div/div[3]/div[2]/button[1]"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent = {}".format(headers['User-Agent']))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(10)
driver.get(URL)

try:
    open('../NASDAQ_DATA/data.csv', 'x')
except:
    pass
file = open('../NASDAQ_DATA/data.csv', 'w')
columns = ['year', 'month', 'day', 'time', 'country', 'event', 'actual', 'consensus', 'previous']
file.write(','.join(columns) + '\n')


# MAIN FUNCTIONS

def get_soup():
    try:
        page = driver.page_source
    except:
        return None
    else:
        try:
            soup = BeautifulSoup(page, "html.parser")
        except:
            return None
        else:
            return soup


def scrape_results(soup, date):
    count = soup.find(name='div', attrs={'class': 'market-calendar__count'}).get_text().split(' ')
    nums = []
    for word in count:
        if word.isnumeric():
            nums.append(int(word))
    get_csv_data(soup, date)
    if len(nums) == 3 and nums[1] < nums[2]:
        next_button = driver.find_element(By.CLASS_NAME, 'pagination__next')
        driver.execute_script('arguments[0].scrollIntoView(false);', next_button)
        driver.execute_script('window.scrollBy(0, 100);', '')
        next_button.click()
        y = driver.find_element(By.CLASS_NAME, "time-belt__prev")
        driver.execute_script('arguments[0].scrollIntoView(true);', y)
        driver.execute_script('window.scrollBy(0, -100);', '')
        new_soup = get_soup()
        if new_soup is not None:
            scrape_results(new_soup, date)


def get_csv_data(soup, date):
    rows = soup.find_all(name='tr', attrs={'class': 'market-calendar-table__row'})
    csv_text = ''
    for row in rows:

        try:
            time = row.find(name='th', attrs={'data-column': 'gmt'}).get_text().strip()
        except:
            time = ''

        try:
            country = row.find(name='td', attrs={'data-column': 'country'}).get_text().strip()
        except:
            country = ''

        try:
            event = row.find(name='td', attrs={'data-column': 'eventName'}).get_text().strip()
        except:
            event = ''

        try:
            actual = row.find(name='td', attrs={'data-column': 'actual'}).get_text().strip()
        except:
            actual = ''

        try:
            consensus = row.find(name='td', attrs={'data-column': 'consensus'}).get_text().strip()
        except:
            consensus = ''

        try:
            previous = row.find(name='td', attrs={'data-column': 'previous'}).get_text().strip()
        except:
            previous = ''

        if len(time) > 0 or len(country) > 0 or len(event) > 0 or len(actual) > 0 or len(consensus) > 0 or len(previous) > 0:
            csv_text += '{},{},{},{},{},{},{},{},{}\n'.format(date['year'], date['month'], date['day'], time, country, event, actual, consensus, previous)
    file.write(csv_text)
    return csv_text


def scrapema():
    start = time.time()
    results = 0
    target_date = {'year': 2015, 'month': 6, 'day': 1, 'hour': 0, 'minute': 0, 'clock': 'AM'}
    date = TimeStruct(time.time())
    yesterday = TimeStruct(date.stamp - 24 * 3600)
    terminate = TimeStruct(TimeStamp(target_date, time.time()).convert())
    while date.stamp >= terminate.stamp:
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
                scrape_results(soup, date.cumulative())
                results += 1
                print('results: {}\ttime: {}'.format(results, time.time() - start))
        time_buttons = driver.find_elements(By.CLASS_NAME, "time-belt__item")
        yesterday_button = None
        yesterday_struct = yesterday.cumulative()
        for button in time_buttons:
            if (yesterday_struct['year'] == int(button.get_dom_attribute('data-year')) and
                    yesterday_struct['month'] == int(button.get_dom_attribute('data-month')) and
                    yesterday_struct['day'] == int(button.get_dom_attribute('data-day'))):
                yesterday_button = button
        if yesterday_button is not None:
            yesterday_button.click()
            try:
                driver.find_element(By.CLASS_NAME, 'time-belt__prev').click()
            except:
                pass
        date = yesterday
        yesterday = TimeStruct(yesterday.stamp - 24 * 3600)


scrapema()
