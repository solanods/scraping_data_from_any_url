import time
import re
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#============================GLOBAL NAMESPACE======================================================
START_URL = 'https://rs.olx.com.br'
USERNAME = 'xxxxxxxxxxxxx@outlook.com'
PASSWORD = 'xxxxxxxxxxxxxx'

#============================LOGIN================================================================
driver.get(START_URL)
driver.maximize_window()
driver.find_element(By.LINK_TEXT, 'Entrar').click()
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[1]/div[2]/form/div[1]/div[2]/input').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[1]/div[2]/form/div[2]/div[2]/div/div/input').send_keys(PASSWORD)
time.sleep(4)
driver.find_element(By.CSS_SELECTOR, '.kgGtxX').click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, '.hguzci').click()#botão fazer isso depois

#======================================SEARCH====================================================

# open the first search link
driver.get('https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/grande-porto-alegre/novo-hamburgo/imoveis/venda/casas')

#get all the links from the first page
ads_links = []
links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
    ads_links.append(link.get_attribute('href'))
#================================CLEAN THE LINKS=================================================

# Remove none objects
ads_links = [link for link in ads_links if isinstance(link, str)]

# Get the pagination links only to inspect the pattern
pagination_links = [link for link in ads_links if re.search(r'.+o=\d+$', link)]

# The strings we are looking for - houses links - finish with 9 digits in sequence
houses_links = [link for link in ads_links if re.search(r'.+\d{9}$', link)]
time.sleep(4)

#==========CRAWL AND CLEAN THE LINKS USING A LOOP FOR PAGINATION=================================

sale_links = []
for i in range(2, 7):
    driver.get(f'https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/grande-porto-alegre/novo-hamburgo/imoveis/venda/casas?o={i}')
    time.sleep(4)
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        sale_links.append(link.get_attribute('href'))

sale_links = [link for link in sale_links if isinstance(link, str)]
sale_links = [link for link in sale_links if re.search(r'.+\d{9}$', link)]

#===========================================CREATE A DATAFRAME EXAMPLE====================
#create one list for each df column
links = []
titles = []
prices = []

for link in sale_links[:10]:
    driver.get(link)
    driver.maximize_window()
    links.append(link)
    titles.append(driver.find_element(By.TAG_NAME, 'h1').text)
    prices.append(driver.find_element(By.CSS_SELECTOR, '.eQLrcK').text)
    # zip the columns
    df = pd.DataFrame(list(zip(links, titles, prices)), columns=['Link', 'Titles', 'Prices'])

driver.close()






