"""This bot will scrape links from a site with scroll"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get("https://www.autocarro.com.br/particular")
driver.maximize_window()


ads_links = []
while True:
    try:
        links = driver.find_elements(By.TAG_NAME, 'a')
        links = [link.get_attribute('href') for link in links]
        ads_links.append([link for link in links if link is not None])
        time.sleep(3)
        #scroll to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'btn-lg-icon--text ').click()
        time.sleep(2)

    except:
        break


# All links in the same list
all_links = []
for i in ads_links:
    all_links.extend(i)


# Filter by substring
all_links = [link for link in all_links if 'https://autocarro.com.br/particular/anuncio/' in link]

# Get owner name, city and phone in each page
names = []
cities = []
phones = []

# Define here the number of pages to scrape
for link in all_links[:5]:
    driver.get(link)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR, '.contact-phone--container .tel').click()
    name = driver.find_element(By.CSS_SELECTOR, '.h1').text
    city = driver.find_element(By.CSS_SELECTOR, '.text-regular').text
    phone = driver.find_element(By.CSS_SELECTOR, '.contact-phone--container .tel').text
    names.append(name)
    cities.append(city)
    phones.append(phone)
    # zip the columns
    df = pd.DataFrame(list(zip(names, cities, phones)), columns=['Name', 'City', 'Phone'])

df.to_csv('autocarro_contacts.csv', index=None)

driver.close()












