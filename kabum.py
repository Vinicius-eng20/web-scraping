from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re, time, math, datetime
import pandas as pd

url = input('Enter the URL: ')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver.get(url)

time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')

qtd_itens = soup.find('div', id='listingCount').get_text().strip()
index = qtd_itens.find(' ')
qtd = qtd_itens[:index]
ultima_pagina = math.ceil(int(qtd) / 20)

# Estrutura de dados para armazenar os resultados
dic_produtos = {
    'LocalVenda': 'Kabum',
    'Marca': '',
    'preco': [],
    'data': datetime.datetime.today().strftime("%d/%m/%y"), 
    'descricao': [], 
    'link': []
}


for i in range(1, ultima_pagina +1):
    url_pag = f'{url}?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    driver.get(url_pag)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        descricao = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip().replace('R$','')
        link = produto.find('a', class_=re.compile('productLink'))['href']

        print(descricao, preco)

        dic_produtos['descricao'].append(descricao)
        dic_produtos['preco'].append(preco)
        dic_produtos['link'].append('https://www.kabum.com.br'+link)

    print(url_pag)

driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_csv('./dados.csv', sep=',', encoding='utf-8')

