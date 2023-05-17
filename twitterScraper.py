import time, urllib.request
import re
import random
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


proxy_list = [
    {'http': 'http://35.233.162.87:3100'},
    {'http': 'http://174.138.184.82:37725'},
    {'http': 'http://204.2.218.145:8080'},
    {'http': 'http://88.99.234.110:2021'},
]

random.shuffle(proxy_list)

for proxy in proxy_list:
    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(400, 900)
driver.set_window_position(800, 0)
driver.get('https://twitter.com/i/flow/login')
time.sleep(5)

# finding input username field
findInputField = driver.find_element(By.CSS_SELECTOR, 'input[name="text"]')
findInputField.send_keys('polte560274')
time.sleep(2)

# clicking on next button
clickNextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]')))
clickNextButton.click()
time.sleep(2)

# finding input password field
findPasswordField = WebDriverWait(driver, 600).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
findPasswordField.send_keys('faizan..12')
time.sleep(2)

# clicking on login button
clickNextButton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Log in")]')))
clickNextButton.click()
time.sleep(2)

# opening twitch account
driver.get('https://twitter.com/anti_juju2')
time.sleep(2)

# clicking on followers button
followersButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Followers")]')))
followersButton.click()
time.sleep(5)

# Scroll to the bottom of the page to load all followers and getting links of accounts
visited_links = set()
last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//section["css-1dbjc4n"]')))
    time.sleep(5)
    # getting followers links
    links = driver.find_elements(By.XPATH,'//a[@class="css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"]')
    for link in links:
        href = link.get_attribute('href')
        if href not in visited_links:
            visited_links.add(href)
            print(href)

    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height
    time.sleep(5)


# Open the accounts of followers
for accountLink in visited_links:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(accountLink)

    try:
        # Extract number of followers
        followers = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href,"/followers")]/span')))
        followers_count_str = followers.text.replace(',', '')

        if 'K' in followers_count_str:
            followers_count = int(followers_count_str.replace('K', '')) * 1000
        elif 'M' in followers_count_str:
            followers_count = int(followers_count_str.replace('M', '')) * 1000000
        else:
            followers_count = int(followers_count_str)

        searchingKeywordInBio = driver.find_element(By.XPATH, '//div[@class="css-1dbjc4n r-1adg3ll r-6gpygo"]')

        if followers_count < 500 and "design" in searchingKeywordInBio.text.lower():
            print("Condition satisfied, sending follow request.")
            print("Followers:", followers_count, "\nBio:",searchingKeywordInBio.text, "\n")

        else:
            print("Condition not satisfied\n")
        time.sleep(3)

    except Exception as e:
        print(e)

    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

time.sleep(5)
driver.quit()

