import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
__import__("dotenv").load_dotenv()

username = os.environ["RUT"]
password = os.environ["PASSWORD"]

driver = webdriver.Firefox()
driver.maximize_window()
driver.implicitly_wait(15)

driver.get("https://www.bancofalabella.cl/")

driver.find_element(By.ID, "login-button").click()

driver.find_element(By.ID, "user").send_keys(username)
pswd = driver.find_element(By.ID, "password")

pswd.send_keys(password)
pswd.submit()

try:
    boldemord = driver.find_element(By.CLASS_NAME, "dy-lb-close")
    boldemord.click()
except:
    print("Adios maldito pop-up")

driver.find_element(By.ID, "accountDetail0").click()

tabla = driver.find_element(By.ID, "ctbListMovbfch")

outerHTML = tabla.get_attribute("outerHTML")

df = pd.read_html(outerHTML)[0]

print(df)

df.to_csv("cartola.csv")
