from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}

# Função para obter as URLs das páginas seguintes
def get_next_page_url(soup):
    next_button = soup.find('li', class_='andes-pagination__button--next')
    if next_button:
        link_next_page = next_button.find('a')
        if link_next_page:
            return link_next_page.get('href')
    return None

class Scraping:
    def mercado_livre(self, url):
        current_url = url

        lista_json = []
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
                    price = re.sub(r'[^0-9,]', '', price_text).replace(',', '.')
                link = produto.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')['href']

                lista_json.append({
                    'titulo': titulo,
                    'price': price,
                    'link': link,
                })
            
            # Obtém a URL da próxima página
            current_url = get_next_page_url(soup)
            
            # Imprime a URL da próxima página (ou pode fazer algo mais com ela)
            if current_url:
                print("URL da próxima página:", current_url)
            else:
                print("Nenhuma próxima página encontrada.")

        return lista_json




            

            



