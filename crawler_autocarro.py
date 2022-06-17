"""This bot will scrape links from a site with scroll"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
        time.sleep(3)

    except:
        break


# All links in the same list
all_links = []
for i in ads_links:
    all_links.extend(i)

# Filter by substring
all_links = [link for link in all_links if 'https://autocarro.com.br/particular/anuncio/' in link]






