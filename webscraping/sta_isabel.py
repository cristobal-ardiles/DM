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
driverOptions.add_argument("--headless") #so browser is not displayed
driverService = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=driverService, options=driverOptions)


driver.get("https://www.santaisabel.cl/locales")

#only RM
region_div = driver.find_element(By.CLASS_NAME, "localities-filter")
region = region_div.find_element(By.TAG_NAME, "a")
region.click()

region_div = driver.find_element(By.CLASS_NAME, "localities-filter")
button = region_div.find_element(By.TAG_NAME, "button")
button.click()

#Getting all elements

df = pd.DataFrame(columns=["Nombre", "Direccion"])

#Navigating the page 
soup = BeautifulSoup(driver.page_source)
stores = soup.find_all("article")
for store in stores:
    name = store.find("h1").get_text()
    address = store.find("div", "local-info-content").get_text()
    df.loc[len(df)] = [name, address]

df.to_csv("sta_isabel.csv", index=False)
