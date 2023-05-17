import time, urllib.request
import re
import random
import  instaloader
import selenium.common
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
selenium.common.WebDriverException
import  requests
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



driver=webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(800,900)
driver.set_window_position(500,0)
driver.get("https://www.instagram.com/")


# Login code
time.sleep(5)
username=driver.find_element(By.CSS_SELECTOR ,"input[name='username']")
password=driver.find_element(By.CSS_SELECTOR, "input[name='password']")

username.clear()
password.clear()
username.send_keys("pr.oject1391")
password.send_keys("project..12")
login=driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(3)

#save login info?
time.sleep(3)
notnow_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Not Now')]")))
notnow_button.click()

#turn off notifications
time.sleep(5)
notnow2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now')]")))
notnow2.click()

# search account
time.sleep(5)
accountName="nike"
driver.get('https://www.instagram.com/{}/'.format(accountName))
time.sleep(5)

# Open post
driver.execute_script("window.scrollBy(0, 300);")
divElement = driver.find_elements(By.XPATH, "//div[@class='_aabd _aa8k  _al3l']")
count = 0
postCount=1
for post in divElement:
    if count >= 10:
        print("All 10 post has been scrapped successfully.")
        break
    else:
        post.click()
        time.sleep(2)

        commentsDiv = driver.find_elements(By.XPATH, "//div[@class='_a9zm']")

        for comments in commentsDiv:
            getName = comments.find_element(By.XPATH, ".//a[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp xqnirrm xj34u2y x568u83']").text
            getComment = comments.find_element(By.XPATH, ".//div[@class='_a9zs']").text
            print(getName, "\n", getComment, "\n")
            time.sleep(2)
        print(postCount,"Post Scrapped Succesfully.")
        count += 1
        postCount += 1
        time.sleep(2)
        driver.back()

# open follower
# followers = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href,'/followers/')]")))
# followers.click()
# time.sleep(5)
#
#
# # scroll down to load all followers
# followerList = driver.find_element(By.XPATH, "//div[@class='_aano']")
# for i in range(5):
#     driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followerList)
#     time.sleep(3)
#
#
# # scrape emails of public accounts from the list of followers
# time.sleep(3)
# email_list = []
# profileNames=[]
# follower_links = driver.find_elements(By.XPATH, "//div[@class='xt0psk2']//a")
# print(len(follower_links))
#
# time.sleep(5)
# for link in follower_links:
#     href = link.get_attribute('href')
#     profileUserNames=href.split("/")[-2]
#     profileNames.append(profileUserNames)
#     print(href)
#     print(profileUserNames)
#
#     if href != "":
#         driver.execute_script("window.open('');")
#         driver.switch_to.window(driver.window_handles[-1])
#         driver.get(href)
#         time.sleep(3)
#
#         try:
#             email_link = driver.find_element(By.XPATH, "//div[@class='_aa_c']")
#             bio_text = email_link.text
#             email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#             emails = re.findall(email_pattern, bio_text)
#             if emails:
#                 print(f"Email found: {emails}")
#                 print("_________________________________")
#                 email_list.append(emails)
#             else:
#                 print("Email not found in this account")
#                 print("_________________________________")
#
#         except NoSuchElementException:
#             print("Private Account.")
#             print("_________________________________")
#
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#
# print(f"Email list: {email_list}")




