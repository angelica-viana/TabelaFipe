from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

carros = {}
numero_carro = 0

time.sleep(1)

def seleciona_mes_ano():
    navegador.find_element(By.XPATH,'//*[@id="selectTabelaReferenciacarro_chosen"]/a/div/b').click()
    options_mes_ano = navegador.find_elements(By.XPATH,'//*[@id="selectTabelaReferenciacarro_chosen"]/div/ul')
    return options_mes_ano[0].find_elements(By.CSS_SELECTOR,'li')

def seleciona_marca(indice):
    element_clique = WebDriverWait(navegador,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="selectMarcacarro_chosen"]/a/div/b'))).click()

    options_marca = navegador.find_elements(By.XPATH,'//*[@id="selectMarcacarro_chosen"]/div/ul')

    lista_marca = options_marca[0].find_elements(By.CSS_SELECTOR,'li')

    lista_marca[indice].click() #0 ACURA, #28 FIAT

def seleciona_modelo():
    time.sleep(0.5)
    navegador.find_element(By.XPATH,'//*[@id="selectAnoModelocarro_chosen"]/a/div/b').click()
    options_modelos = navegador.find_elements(By.XPATH,'//*[@id="selectAnoModelocarro_chosen"]/div/ul')
    return options_modelos[0].find_elements(By.CSS_SELECTOR,'li')

def seleciona_ano_modelo():
    navegador.find_element(By.XPATH,'//*[@id="selectAnocarro_chosen"]/a/div/b').click()
    options_ano_modelo = navegador.find_elements(By.XPATH,'//*[@id="selectAnocarro_chosen"]/div/ul')
    return options_ano_modelo[0].find_elements(By.CSS_SELECTOR,'li')

def move_tela(times):
    for time in range(0,times):
        navegador.find_element(By.TAG_NAME,'body').send_keys(Keys.ARROW_UP)
########################################################################################################

start = datetime.now()
print(start)

#Segundo:clicar e selecionar o mes de pesquisa
lista_mes_ano = seleciona_mes_ano()
#for mes_ano in range(0,len(lista_mes_ano)):
for mes_ano in range(0,1):
    lista_mes_ano[mes_ano].click()
    
    seleciona_marca(0)

    #Terceiro:clicar e selecionar a marca
    lista_modelos = seleciona_modelo()

    print(f'Quantidade de modelos = {len(lista_modelos)}\n')
    
    #Quarto: clicar e selecionar o modelo
    for modelo in range(0, len(lista_modelos)):
        print(f'********************** Modelo:{modelo} **********************')

        lista_modelos[modelo].click()

        lista_ano_modelo = seleciona_ano_modelo()

        #Quinto: clicar em ano_modelo e pesquisar
        for ano_modelo in range (0,len(lista_ano_modelo)):
            lista_ano_modelo[ano_modelo].click()

            time.sleep(0.5)
            navegador.find_element(By.LINK_TEXT,'Pesquisar').click()

            #Sexto: salvar os dados da tabela em um dicionários.
            tabela = navegador.find_elements(By.XPATH,'//*[@id="resultadoConsultacarroFiltros"]/table/tbody')
            linhas = tabela[0].find_elements(By.CSS_SELECTOR,'td')

            carro = {}

            for item in range(0,len(linhas)-1,2):
                carro[linhas[item].text] = linhas[item+1].text

            carros[numero_carro] = carro
            print(f'Carro: {carros[numero_carro]}')
            print(15*'-')
            numero_carro += 1
            time.sleep(1)

            move_tela(4)
            time.sleep(1)
            lista_ano_modelo = seleciona_ano_modelo()

        move_tela(8)

        seleciona_marca(1) #reset no campo marca, esse indice precisa ser diferente
                           # da marca que estamos colentando os dados
        time.sleep(1)

        seleciona_marca(0)

        lista_modelos = seleciona_modelo()

    move_tela(7)
    seleciona_marca(1)

    lista_mes_ano = seleciona_mes_ano()

end = datetime.now()
print(end)

navegador.close()

object_json = json.dumps(carros, indent = 2, ensure_ascii = False)
with open('carrosACURA.json','w') as file:
    file.write(object_json)
