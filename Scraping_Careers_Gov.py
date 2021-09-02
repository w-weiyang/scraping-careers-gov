from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys # This allows you to use keys like "Enter", "Space", etc.
import time

import pandas as pd

# INITIALIZING WEB DRIVER
PATH = "C:\Program Files\Chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# OPENING TARGET PAGE THROUGH DRIVER
driver.get("https://careers.pageuppeople.com/688/cwlive/en/listing/")

# INITIALIZE ACTION CHAIN
actions = ActionChains(driver) 
# actions.click() ... If you need to click something
# actions.perform ... actions do not trigger until actions.perform() is run

# INITIAL FILTERING
# Find the search bar, enter your search (e.g. "manager"). The site will auto-filter without the need to press 'Enter'
search_bar = driver.find_element_by_id("search-keyword")
search_bar.send_keys("analyst")
# search_bar.send_keys(Keys.RETURN)... Technically not needed for this site
# search_bar.clear() ... If you want to clear the search field

# SLEEP TO ALLOW TIME FOR (SITE) AUTO-FILTERING
time.sleep(5)

# LOAD ENTIRE LISTING BY FINDING AND CLICKING "MORE JOBS" BUTTON UNTIL IT NO LONGER EXISTS
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

# DRAWING OUT LINKS TO EACH INDIVIDUAL JOB POSTING
Job_links = []
for tr in table.findAll("tr"):
    trs = tr.findAll("td")
    for each in trs:
        try:
            link = 'https://careers.pageuppeople.com/' + each.find('a')['href']
            Job_links.append(link)
        except:
            pass

# APPENDING LINKS TO DATAFRAME JOB_DF
Job_DF['Link'] = Job_links

# EXPORT TO EXCEL FILE
Job_DF.to_excel(r'C:\... <Your Directory> ...\CAG.xlsx', index=False, header=True)




