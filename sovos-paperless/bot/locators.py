from selenium.webdriver.common.by import By

login = (By.NAME, "imageField")
anchors = (By.XPATH, '//img[@src="/Facturacion/images/03gest_aver.gif"]/..')
pag150 = (By.CSS_SELECTOR, ".txtArial09 a[href='javascript:doPagina(6,1,0,3000);']")
despacho = (By.CSS_SELECTOR, "input[name='chkTpoDoc'][value='52']")
fecha_inicio = (By.NAME, "fchemiini")
buscar = (By.NAME, "busq")
salir = (By.ID, "salir")
iframe = (By.TAG_NAME, "iframe")
table = (By.CSS_SELECTOR, "table.txtTrebuchet11")
