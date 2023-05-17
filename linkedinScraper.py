import os
import re
import string
import time, urllib.request
import collections
import pandas as pd
import selenium.common
import tldextract
import csv
import postgrest
import supabase
from geopy.geocoders import Nominatim
from selenium import webdriver
import random
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import  requests
selenium.common.WebDriverException
from itertools import cycle
from geopy.geocoders import Nominatim
from dateutil import parser
from mtranslate import translate
from datetime import datetime, timedelta
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


proxy_list = [

    {'ip': '114.233.50.121', 'port': 1080,   'protocol': 'SOCKS4'},
    {'ip': '93.91.118.141',  'port': 3629,   'protocol': 'socks4'},
    {'ip': '100.2.103.26',   'port': 8080,   'protocol': 'socks4'},
    {'ip': '103.120.202.53', 'port': 5678,   'protocol': 'socks4'},
    {'ip': '146.59.243.35',  'port': 27445,  'protocol': 'SOCKS4'},
    {'ip': '114.105.221.202','port': 38801,  'protocol': 'SOCKS4'},
    {'ip': '77.238.79.111',  'port': 5678,   'protocol': 'SOCKS4'},
]

proxy_pool = cycle(proxy_list)

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(800, 900)
driver.set_window_position(400, 0)
driver.get('https://www.linkedin.com/jobs/search?keywords=&location=WorldWide&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')

# check if visitedLink.csv exist?
header = ['Visited Links']
with open('visitedLinks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# job post array
job_post_array =[]

# scrolling the web page
visited_links = set()

while True:
    try:
        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            # check if the "See More Jobs" button is visible
            see_more_button = driver.find_element(By.XPATH, '//button[contains(text(), "See more jobs")]')
            if see_more_button.is_displayed():
                see_more_button.click()
                time.sleep(2)
                # scroll down to the bottom of the page again
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)
                # reset the last height
                last_height = driver.execute_script('return document.body.scrollHeight')
            else:
                break

            job_links = driver.find_elements(By.XPATH,'//a[@class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]" and @href]')

            for link in job_links:
                href = link.get_attribute('href')
                if href not in visited_links:
                    visited_links.add(href)

                    try:
                        # open link in new window with a new proxy
                        proxy = next(proxy_pool)
                        proxy_string = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
                        webdriver.DesiredCapabilities.CHROME['proxy'] = {
                            "httpProxy": proxy_string,
                            "ftpProxy": proxy_string,
                            "sslProxy": proxy_string,
                            "proxyType": "MANUAL"
                        }

                        driver.execute_script("window.open('" + href + "', '_blank');")
                        time.sleep(2)

                        driver.switch_to.window(driver.window_handles[-1])  # switch to new window
                        try:

                            with open('visitedLinks.csv', 'r') as file:
                                reader = csv.reader(file)
                                for row in reader:
                                    if href in row:
                                        print('\nThis job has already been scraped')
                                    else:
                                        # getting job details
                                        job_title = WebDriverWait(driver, 1).until( EC.presence_of_element_located((By.XPATH,'//h1[@class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"]'))).text
                                        translate_title = translate(job_title)
                                        job_title = translate_title

                                        company_div_element = driver.find_element(By.XPATH, '//div[@class="topcard__flavor-row"]')
                                        get_company_name = company_div_element.find_element(By.XPATH,'./span[@class="topcard__flavor"]/a').text
                                        translate_comp= translate(get_company_name)
                                        get_company_name = translate_comp

                                        get_location=company_div_element.find_element(By.XPATH,'./span[@class="topcard__flavor topcard__flavor--bullet"]').text
                                        split_location=get_location.split(',')[0]
                                        time.sleep(2)

                                        # Scroll job section
                                        time.sleep(1)
                                        driver.execute_script("window.scrollBy(0, 450);")
                                        find_job_details=driver.find_elements(By.XPATH,'//li[@class="description__job-criteria-item"]')

                                        try:
                                            click_show_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                                              '//button[@class="show-more-less-html__button show-more-less-html__button--more"]')))
                                            click_show_more.click()
                                            get_job_description = driver.find_element(By.XPATH,
                                                                                      '//div[@class="show-more-less-html__markup"]').text
                                            get_job_description = get_job_description.replace('\n', ' ')
                                            translate_desc=translate(get_job_description)
                                            get_job_description=translate_desc

                                        except TimeoutException:
                                            get_job_description = driver.find_element(By.XPATH,
                                                                                      '//div[@class="show-more-less-html__markup"]').text
                                            get_job_description = get_job_description.replace('\n', ' ')
                                            translate_desc=translate(get_job_description)
                                            get_job_description=translate_desc


                                        find_location_type=driver.find_element(By.XPATH, '//section[@class="top-card-layout container-lined overflow-hidden babybear:rounded-[0px]"]').text

                                        if find_location_type == "On-site" or find_location_type == "Remote" or find_location_type == "Hybrid":
                                            get_location_type=find_location_type
                                        else:
                                            options = ["remote", "hybrid", "onsite"]
                                            get_location_type = random.choice(options)

                                        time.sleep(2)
                                        # open company profile
                                        find_company_profile = driver.find_element(By.XPATH,'//span[@class="topcard__flavor"]')
                                        get_company_profile=find_company_profile.find_element(By.XPATH, './a[@class="topcard__org-name-link topcard__flavor--black-link"]')
                                        href_link = get_company_profile.get_attribute('href')


                                        time.sleep(2)
                                        # find website link
                                        try:
                                            pattern = r'http?://\S+'
                                            website_url = re.findall(pattern, get_job_description)[0]
                                        except IndexError:
                                            company_name = href_link.split('/')[-1].split('?')[0]  # extract the company name from URL
                                            company_name = ''.join(company_name.split('-'))  # combining string
                                            website_name = company_name
                                            extracted = tldextract.extract(website_name)
                                            tld = "com"  # Set the TLD manually
                                            website_url = f"http://www.{website_name}.{tld}"

                                        time.sleep(2)
                                        # find years of experience
                                        regex = r"\d+ years? of experience.*?(?=in|with)"
                                        matches = re.findall(regex, get_job_description, re.IGNORECASE)
                                        if matches:
                                            years_of_experience = int(matches[0].split()[0])
                                            get_expereince=years_of_experience
                                        else:
                                            get_expereince="No Experience mentioned"

                                        time.sleep(2)
                                        # find date posted
                                        find_date = driver.find_element(By.XPATH,
                                                                        '//section[@class="top-card-layout container-lined overflow-hidden babybear:rounded-[0px]"]').text
                                        time_pattern = re.compile(r'(\d+\s\w+)\sago')
                                        timematch = time_pattern.search(find_date)
                                        if timematch:
                                            get_date_posted = timematch.group()
                                            job_posted_time = get_date_posted

                                            # Parse the job posting time
                                            posted_date = datetime.now()
                                            if "week" in job_posted_time:
                                                weeks_ago = int(job_posted_time.split()[0])
                                                posted_date = datetime.now() - timedelta(weeks=weeks_ago)
                                            elif "day" in job_posted_time:
                                                days_ago = int(job_posted_time.split()[0])
                                                posted_date = datetime.now() - timedelta(days=days_ago)
                                            elif "hour" in job_posted_time:
                                                hours_ago = int(job_posted_time.split()[0])
                                                posted_date = datetime.now() - timedelta(hours=hours_ago)

                                            # Format the date as per your requirement
                                            formatted_date = posted_date.strftime("%Y-%m-%d")
                                        else:
                                            get_date_posted = "Today"

                                        time.sleep(1)
                                        elements=[]
                                        for Text in find_job_details:
                                            extract_text=Text.find_element(By.XPATH, './span[@class="description__job-criteria-text description__job-criteria-text--criteria"]').text
                                            elements.append(extract_text)

                                        time.sleep(2)
                                        # Find salary
                                        salary_pattern = r'\$\d+(?:,\d+)*(?:\.\d+)?\s*(?:per\s+)?\b(?:year|month|week|hour)\b'
                                        salary_matches = re.findall(salary_pattern, get_job_description)
                                        if salary_matches:
                                            get_salary=salary_matches
                                        else:
                                            get_salary="Salary not mentioned"

                                        time.sleep(2)
                                        # Find Country
                                        geolocator = Nominatim(user_agent='my-kskdkk')
                                        location = geolocator.geocode(get_location)
                                        if location:
                                            country = location.raw['display_name'].split(',')[-1].strip()
                                            country_name=country
                                            translated_text = translate(country_name)
                                            country_name=translated_text

                                        else:
                                            country_name="Unknown"

                                        # find job type
                                        time.sleep(2)
                                        get_job_type=elements[1]
                                        get_job_category=elements[3]
                                        time.sleep(2)

                                        job_board="Linkedin"
                                        job_board_link ="https://www.linkedin.com/"

                                        # print all details
                                        print("\nJob Title:",job_title,
                                              "\nCompany Name:",get_company_name,
                                              "\nCountry Name:",country_name,
                                              "\nApplication Link:",href,
                                              "\nJob Type:",get_job_type,
                                              "\nJob Category:",get_job_category,
                                              "\nJob Description:",get_job_description,
                                              "\nLocation Type:",get_location_type,
                                              "\nCompany Website:",website_url,
                                              "\nYears of experience:",get_expereince,
                                              "\nSalary:",get_salary,
                                              "\nLocation:",split_location,
                                              "\nDate Posted:",formatted_date,
                                              "\nJob Board:",job_board,
                                              "\nJob Board Link:",job_board_link,"\n")

                                        # Create a new DataFrame from the new link
                                        new_links = set([href])
                                        new_links_df = pd.DataFrame({'Visited Links': list(new_links)})

                                        # Check if the file exists
                                        if os.path.isfile("visitedLinks.csv"):
                                            df = pd.read_csv("visitedLinks.csv")  # Read the existing CSV file
                                            df = pd.concat([df, new_links_df], ignore_index=True)
                                        else:
                                            df = new_links_df

                                        df.to_csv("visitedLinks.csv", index=False)

                                        # create a tuple of job post information
                                        job_post_tuple = (get_company_name, job_title, split_location, country_name, get_job_category,
                                                          get_job_type, get_location_type, get_job_description, get_salary,
                                                          get_expereince, formatted_date, href, website_url,
                                                          job_board, job_board_link)
                                        # append the tuple to the job_post_array list
                                        job_post_array.append(job_post_tuple)

                                        # create a DataFrame from the job_post_array list
                                        df = pd.DataFrame(job_post_array,
                                                          columns=["Company Name", "Job Title", "Location", "Country", "Job Category","Job Type",
                                                                   "Location Type", "Description", "Salary", "Years of Experience",
                                                                   "Date Posted", "Application Link", "Website Link", "Job_Board", "Job_Board_Link"])

                                        df.to_csv("linkedin_data.csv", index=False)

                                        # Set up Supabase client
                                        SUPABASE_URL = 'https://zxzrwjhmjzesxktrijca.supabase.co'
                                        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4enJ3amhtanplc3hrdHJpamNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODM5OTY2MTUsImV4cCI6MTk5OTU3MjYxNX0.g62cT0Bls3IsHl-7vZfiDQZvtkJHwOIJXimZ58O-Yho'
                                        supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

                                        # Open the CSV file
                                        with open('linkedin_data.csv', 'r', encoding='latin1') as csvfile:
                                            csvreader = csv.reader(csvfile)

                                            field_names = next(csvreader)
                                            data = [dict(zip(field_names, row)) for row in csvreader]

                                        # Insert the data into Supabase table
                                        table_name = 'job101'
                                        try:
                                            response = supabase_client.table(table_name).insert(data).execute()
                                        except postgrest.exceptions.APIError as e:
                                            print(e)

                                        # Check if the insertion was successful
                                        if response is not None:
                                            print('Data inserted into supabase successfully')

                                        else:
                                            print('Error while inserting data')
                                            print(response.text)


                        finally:
                            driver.close()  # close new window
                            driver.switch_to.window(driver.window_handles[0])  # switch back to original window

                    except Exception as e:
                        print(e)

                else:
                    continue
        time.sleep(3)

    except Exception as e:
        print("Error: ", e)

time.sleep(10)
driver.quit()
