import os
import pandas as pd
import locators
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
__import__("dotenv").load_dotenv()

rut = os.environ['RUT']
password = os.environ['password']

empresa = '762156288'

BASE_URL = 'https://www.officebanking.cl'

driver = webdriver.Firefox()
driver.implicitly_wait(10)

driver.get(BASE_URL)

driver.find_element(*locators.rut).send_keys(rut)
clave = driver.find_element(*locators.password)
clave.send_keys(password)
clave.submit()

frame = driver.find_element(*locators.nuestroFrame)

driver.switch_to.frame(frame)

tablaInicio = driver.find_element(*locators.tablaInicio)
data = (tablaInicio.get_attribute('outerHTML'))

print(pd.read_html(data)[0]["Rut Empresa"])

button = driver.find_element(*locators.button).click()

driver.get(BASE_URL + '/EOB/Redirect.asp?cod_srv=TRNCNA_CTLCRR')

tablaMovimientos = driver.find_element(*locators.tablaMovimientos)

btnExcel = driver.find_element(*locators.btnExcel)

driver.execute_script("arguments[0].click();", btnExcel)

sleep(300000)

driver.quit()
