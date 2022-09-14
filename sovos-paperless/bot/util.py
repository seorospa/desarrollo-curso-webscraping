from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
from . import locators
import os

BASE_URL = "https://asp4.paperless.cl/Facturacion"
REMOTE_URL = os.environ.get("REMOTE_URL")

old_cols = ["Tipo de Documento", "Fecha de Recepción", "Fecha de Emisión", "RUT Emisor", "Folio", "Monto"]
new_cols = ['doc_type', 'reception_date', 'submit_date', 'issuer_rut', 'invoice', 'amount']


class WebDriver(webdriver.Firefox):
    def __init__(self):
        #super(command_executor=REMOTE_URL, options=Options())
        super().__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def login(self, cred):
        self.get(BASE_URL)

        elements = (
            ("txtRut", cred["rut"]),
            ("txtLogin", cred["user"]),
            ("txtPasswd", cred["password"])
        )

        for n, p in elements:
            self.find_element(By.NAME, n).send_keys(p)

        self.find_element(*locators.login).click()

    def get_urls(self, from_date):
        self.get(BASE_URL + "/parte4/documentos/busqueda_documentos.jsp")
        self.find_element(*locators.despacho).click()

        inicio = self.find_element(*locators.fecha_inicio)
        inicio.clear()
        inicio.send_keys(from_date.strftime('%d-%m-%Y'))

        try:
            self.find_element(*locators.buscar).click()
            self.find_element(*locators.pag150).click()
            elements = self.find_elements(*locators.anchors)
        except NoSuchElementException:
            print("sin registros")
            return []

        return [x.get_attribute("href") for x in elements]

    def process_url(self, company_rut: str, url: str) -> pd.DataFrame:
        self.get(url)

        iframe = self.find_element(*locators.iframe)
        src = iframe.get_attribute("src")

        element = self.find_element(*locators.table)
        html = element.get_attribute('outerHTML')

        rename = dict(zip(old_cols, new_cols))

        html_df = pd.read_html(html, index_col=0)[0].T[old_cols]
        df = html_df.rename(columns=rename)

        df['reception_date'] = pd.to_datetime(df['reception_date'], format='%d-%m-%Y%H:%M:%S')
        df['submit_date'] = pd.to_datetime(df['submit_date'], format='%d-%m-%Y')
        df['amount'] = pd.to_numeric(df['amount'].str.replace("[. $]", "", regex=True))
        df['invoice'] = pd.to_numeric(df['invoice'].str.replace(".", "", regex=False))
        df["url"] = src
        df["company_rut"] = company_rut
        df["downloaded"] = False

        return df

    def logout(self):
        self.find_element(*locators.salir).click()
