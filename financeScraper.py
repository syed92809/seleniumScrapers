import time, urllib.request
import re
import random
import pandas as pd
import xls_writer
import  instaloader
import selenium.common
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import  requests
selenium.common.WebDriverException
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(400, 900)
driver.set_window_position(800, 0)
driver.get("https://finance.yahoo.com/most-active")
time.sleep(5)

driver.execute_script("window.scrollBy(0, 1500);")
time.sleep(2)

data_dict = {}

# getting symbols
symbols = driver.find_elements(By.XPATH, "//a[@class='Fw(600) C($linkColor)']")
time.sleep(2)

for link in symbols:
    symbol_link = link.get_attribute('href')
    print(symbol_link)
    symbol_name = symbol_link.split("/")[4]
    getSymbolName = symbol_name.split('=')[1]
    print(getSymbolName)

    driver.execute_script("window.open('" + symbol_link + "', 'new_window')")
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[-1])

    driver.get(
        'https://finance.yahoo.com/quote/{}/history?period1=1672099200&period2=1679875200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'.format(
            getSymbolName))
    time.sleep(3)
    driver.refresh()

    price_element = driver.find_element(By.XPATH, "//fin-streamer[@data-test='qsp-price']")
    price = float(price_element.get_attribute("value"))
    print("Price of {} is {}".format(getSymbolName, price))

    if price > 200:
        print("Scraping Data....")
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table")))
        rows = table.find_elements(By.XPATH, ".//tr")
        time.sleep(2)

        data = []
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td")
            row_data = []
            for cell in cells:
                row_data.append(cell.text)
            data.append(row_data)

        data_dict[getSymbolName] = data
        print("Data Saved!")
    else:
        print("Price is below 200")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.quit()

writer = pd.ExcelWriter("symbol_data.xlsx", engine='xlsxwriter')

for symbol, data in data_dict.items():
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name=symbol)

print("Data saved in symbol_data.xlsx")
writer.close()