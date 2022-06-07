from bs4 import BeautifulSoup
import lxml
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select


# Setting up browser driver
binary = "/snap/bin/firefox"
driverOptions = webdriver.FirefoxOptions()
driverOptions.binary_location=binary
driverOptions.add_argument("--headless") #so browser is not displayed
driverService = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=driverService, options=driverOptions)

driver.get("https://buysmartstatic.lider.cl/landing/json/storeListHtml.html")

# Displaying 100 rows and only RM
select = Select(driver.find_element_by_name("dtBasicExample_length"))
select.select_by_visible_text("100")

finder_div = driver.find_element_by_id("dtBasicExample_filter")
finder = finder_div.find_element_by_tag_name("input")
finder.click()
finder.send_keys("Metropolitana")


page2 = driver.find_element_by_id("dtBasicExample_next")

#Setting up pandas df to save information
df = pd.DataFrame(columns=["Nombre", "Comuna", "Direccion", "Region"])

page = 1
soup = BeautifulSoup(driver.page_source)
while page <= 2:
    for row in soup.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        values = []
        i=0
        for value in cells:
            if i in [0,1,2,4]:
                text = value.get_text() if i!=0 else value.get_text().strip(' ').strip("\n").strip(" ")
                values.append(value.get_text())
            i+=1
        df.loc[len(df)] = values
    page+=1
    if page == 1:
        page2.click() 
    soup = BeautifulSoup(driver.page_source)

df.to_csv("lider.csv",index=False)

    

