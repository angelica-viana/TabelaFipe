from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime

import json

navegador = webdriver.Chrome()

navegador.get("https://veiculos.fipe.org.br/")
navegador.maximize_window()

#Ordem dos cliques

#Primeiro: clicar em consulta de carros e utilitários pequenos
elemento = WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
    (By.XPATH,'//*[@id="front"]/div[1]/div[2]/ul/li[1]/a/div[2]'
))).click()

time.sleep(1)

def seleciona_mes_ano():
    navegador.find_element(By.XPATH,'//*[@id="selectTabelaReferenciacarro_chosen"]/a/div/b').click()
    options_mes_ano = navegador.find_elements(By.XPATH,'//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul')
    return options_mes_ano[0].find_elements(By.CSS_SELECTOR,'li')

def seleciona_marca():
    navegador.find_element(By.XPATH,'//*[@id="selectMarcacarro_chosen"]/a/div/b').click()
    options_marca = navegador.find_elements(By.XPATH,'//*[@id="selectMarcacarro_chosen"]/div/ul')
    return options_marca[0].find_elements(By.CSS_SELECTOR,'li')

start = datetime.now()
print(start)

lista_mes_ano = seleciona_mes_ano()

mes_ano = {}

for item in range(0, len(lista_mes_ano)):
    mes_ano[item] = lista_mes_ano[item].text
    
lista_marca = seleciona_marca()
marcas = {}

for item in range(0, len(lista_marca)):
    marcas[item] = lista_marca[item].text
    
navegador.close()

object_json = json.dumps(mes_ano, indent= 2, ensure_ascii= False)
with open ('mes_ano.json', 'w') as file:
    file.write(object_json)        

object_json = json.dumps(marcas, indent= 2, ensure_ascii= False)
with open ('marcas.json', 'w') as file:
    file.write(object_json)   
    
end = datetime.now()
print(end)         
    
    


    
