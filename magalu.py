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

qtd_items = soup.find('div', {'data-testid': 'mod-searchheader'})
for qtd in qtd_items:
    qtde = qtd.find('p').text.strip().replace('.','')
index = qtde.find(' ')
qtd = qtde[:index]
ultima_pagina = math.ceil(int(qtd) / 52)

dic_produtos = {
    'LocalVenda': 'Magalu',
    'Marca': '',
    'preco': [],
    'data': datetime.datetime.today().strftime("%d/%m/%y"), 
    'descricao': [], 
    'link': []
}

for i in range(1, ultima_pagina +1):
    url_pag = f'{url}?page={i}'
    driver.get(url_pag)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    produtos = soup.find_all('a', {'data-testid': 'product-card-container'})

    for produto in produtos:
        descricao = produto.find('h2', {'data-testid': 'product-title'})
        preco = produto.find('p', {'data-testid': 'price-value'})
        link = 'https://www.magazineluiza.com.br' + produto['href']
        
        if descricao is not None:
            dic_produtos['descricao'].append(descricao.text.strip())
            dic_produtos['preco'].append(preco.text.strip().replace('R$', ''))
            dic_produtos['link'].append(link)

    print(url_pag)

driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_csv('./dados.csv', sep=',', encoding='utf-8')

print('Finalizado com sucesso.')




