from ast import arg
from curses import beep
import sys
from bs4 import BeautifulSoup
import lxml
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

# Setting up browser driver
binary = "/snap/bin/firefox"
driverOptions = webdriver.FirefoxOptions()
driverOptions.binary_location=binary
# driverOptions.add_argument("--headless") #so browser is not displayed
driverService = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=driverService, options=driverOptions)

driver.get("https://www.tottus.cl/horario-tiendas")

#dataframe
df = pd.DataFrame(columns=["Nombre"])

#Navigating the page 
soup = BeautifulSoup(driver.page_source)
for row in soup.find("table").find_all("tr"):
    info = row.find_all("td")[0].get_text() 
    df.loc[len(df)] = [info]

df.to_csv("tottus.csv", index=False)