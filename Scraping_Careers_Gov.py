from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys # This allows you to use keys like "Enter", "Space", etc.
import time

import pandas as pd

# Initializing Web Driver
PATH = "C:\Program Files\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Opening target page through Driver
driver.get("https://careers.pageuppeople.com/688/cwlive/en/listing/")

# Initialzing action chain
actions = ActionChains(driver) 
# actions.click()
# actions.perform ... actions do not trigger until actions.perform() is run

# Find the search bar, enter your search (e.g. "manager"), then press Enter (Keys.Return)
search_bar = driver.find_element_by_id("search-keyword")
search_bar.send_keys("analyst")
# search_bar.send_keys(Keys.RETURN)
# search_bar.clear() ... If you want to clear the search field

time.sleep(5)
x = True

while x == True:
    try:
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'More'))
            )
        actions.move_to_element(element).perform()
        element.click()
    except:
        x = False
        pass

# HANDING SELENIUM OFF TO BEAUTIFULSOUP
soup = BeautifulSoup(driver.page_source, 'lxml')
table = soup.find('table')

# EXTRACTING TABLE TO DATAFRAME
Job_DF = pd.read_html(driver.page_source)[0]
# pd.read_html(...) provides you with a list of dataframe objects. If you want a table, you need to use the index, [0] in this case, to access it.

Job_links = []
for tr in table.findAll("tr"):
    trs = tr.findAll("td")
    for each in trs:
        try:
            link = 'https://careers.pageuppeople.com/' + each.find('a')['href']
            Job_links.append(link)
        except:
            pass

Job_DF['Link'] = Job_links
Job_DF.to_excel(r'C:\Users\Wong\Desktop\Learning\Web Scraping\Selenium\CAG.xlsx', index=False, header=True)


# "More Results" Link
#more_results = driver.find_element(By.XPATH, '//div[@id="recent-jobs"]/p/a')
#more_results.click()




# CLicking Links through Link Text (Link text only, not title = "xxx")
# link = driver.find_element_by_link_text("...")
# link.click()

# HANDING SELENIUM OFF TO BEAUTIFULSOUP
#soup = BeautifulSoup(driver.page_source, 'lxml')
#print(soup)


