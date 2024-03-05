from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests, re, time, math
from datetime import date

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}

# Função para obter as URLs das páginas seguintes (mlbr)
def get_next_page_url(soup, classe):
    next_button = soup.find('li', class_=classe)
    if next_button:
        link_next_page = next_button.find('a')
        if link_next_page:
            return link_next_page.get('href')
    return None

lista_json = []

class Scraping:
    def get_mlbr(self, url):
        current_url = url

        # Loop para percorrer todas as páginas
        while current_url:
            response = requests.get(current_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Se você quiser fazer algo com a página atual, faça aqui
            produtos = soup.find_all('li', class_='ui-search-layout__item')

            for produto in produtos:
                titulo = produto.find('h2', class_='ui-search-item__title').text.strip()
                price_text = produto.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript')
                if price_text:
                    price_text = price_text.text.strip()
                    price = re.sub(r'[^0-9,]', '', price_text)
                link = produto.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')['href']

                lista_json.append({
                    'LocalVenda': 'MLBR', 
                    'marca': '',
                    'price': price,
                    'data': date.today().strftime(("%d/%m/%y")),
                    'idade': '',
                    'titulo': titulo,
                    'link': link,
                })
            
            # Obtém a URL da próxima página
            current_url = get_next_page_url(soup, 'andes-pagination__button--next')
            
            # Imprime a URL da próxima página (ou pode fazer algo mais com ela)
            if current_url:
                print("URL da próxima página:", current_url)
            else:
                print("Nenhuma próxima página encontrada.")

        return lista_json
    
    def get_kbm(self, url):
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

        for i in range(1, ultima_pagina +1):
            url_pag = f'{url}?page_number={i}&page_size=20&facet_filters=&sort=most_searched&variant=catalog'

            driver.get(url_pag)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            produtos = soup.find_all('div', class_=re.compile('productCard'))

            for produto in produtos:
                descricao = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
                preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip().replace('R$','')
                link = produto.find('a', class_=re.compile('productLink'))['href']

                lista_json.append({
                    'LocalVenda': 'KBM', 
                    'marca': '',
                    'price': preco,
                    'data': date.today().strftime(("%d/%m/%y")),
                    'idade': '',
                    'titulo': descricao,
                    'link': link,
                })
            print(url_pag)

        driver.quit()
        return lista_json
    
    def get_mglu(self, url):
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
                    lista_json.append({
                        'LocalVenda': 'MGLU', 
                        'marca': '',
                        'price': preco.text.strip().replace('R$', ''),
                        'data': date.today().strftime(("%d/%m/%y")),
                        'idade': '',
                        'titulo': descricao.text.strip(),
                        'link': link,
                    })

            print(url_pag)

        driver.quit()
        return lista_json
        
    





            

            



