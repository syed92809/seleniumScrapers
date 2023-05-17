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

productLinksArray=['https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/product/268028767/16684690344/',
                   'https://shopee.sg/Cha-Tra-Mue-3-In-1-Thai-Tea-Instant-Tea-Powder-3in1-500g-i.268028767.21460688628?sp_atk=05090edf-8e57-41d5-9d87-d790dfe0efbe&xptdk=05090edf-8e57-41d5-9d87-d790dfe0efbe',
                   'https://shopee.sg/Cha-Tra-Mue-3-In-1-Thai-Tea-Instant-Tea-Powder-3in1-500g-i.268028767.21460688628?sp_atk=05090edf-8e57-41d5-9d87-d790dfe0efbe&xptdk=05090edf-8e57-41d5-9d87-d790dfe0efbe',
                   'https://shopee.sg/Cha-Tra-Mue-3-In-1-Thai-Tea-Instant-Tea-Powder-3in1-500g-i.268028767.21460688628?sp_atk=05090edf-8e57-41d5-9d87-d790dfe0efbe&xptdk=05090edf-8e57-41d5-9d87-d790dfe0efbe',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886',
                   'https://shopee.sg/product/268028767/18148865886'

                   ]


driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(400, 900)
driver.set_window_position(800, 0)

for links in productLinksArray:
    driver.get(links)
    driver.execute_script("window.scrollBy(500, 200);")
    time.sleep(2)

    productPrice=driver.find_element(By.XPATH, '//div[@class="pqTWkA"]')
    print("Product Price: ",productPrice.text)
    time.sleep(2)

    findMOQ=driver.find_element(By.XPATH, '//input[@class="EquXA8 Wrmraq"]')
    getMOQ=findMOQ.get_attribute('value')
    print("Product MOQ: ",getMOQ)
    print("\n\n")
    time.sleep(2)
driver,quit()

