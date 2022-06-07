from ast import arg
from curses import beep
import sys
from bs4 import BeautifulSoup
import lxml
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# Setting up browser driver
binary = "/snap/bin/firefox"
driverOptions = webdriver.FirefoxOptions()
driverOptions.binary_location=binary
# driverOptions.add_argument("--headless") #so browser is not displayed
driverService = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox(service=driverService, options=driverOptions)


driver.get("https://locales.unimarc.cl/locales_unimarc/")

#Getting all elements
df = pd.DataFrame(columns=["Nombre", "Direccion", "Comuna"])

#only RM
region_select = Select(driver.find_element(By.ID, "regiones"))
region_select.select_by_value("metropolitana")
comuna_select = Select(driver.find_element(By.ID,"comunas"))

for option in comuna_select.options:
    if option.get_attribute("value") == "":
        continue
    option.click()
    soup = BeautifulSoup(driver.page_source, "lxml")
    stores = soup.find(id="panel").find_all("div", "lista")
    for elem in stores:
        name = elem.find("h2").get_text()
        direccion = elem.find("p").get_text()
        comuna = elem.find("span").get_text()
        df.loc[len(df)] = [name, direccion, comuna]

df.to_csv("unimarc.csv", index=False)
