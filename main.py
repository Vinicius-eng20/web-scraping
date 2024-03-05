from scraping import Scraping
import pandas as pd

produtos = Scraping()

print()
url = input('Enter the URL: ')
print()

lista_produtos = produtos.get_kbm(url)
# lista_produtos = produtos.get_mlbr(url)
# lista_produtos = produtos.get_mglu(url)

eliminar = ['Cabo', 'Espelho', 'Mostruario', 'Mostruário', 'Nf', 'nf', 'Fiscal', 'Entrega', 'Usado', 'Desconto', 'Peças', 'Kit', 'Garantia', 'Nfe', 'Nf-e']

lista_filtrada = [
    produto for produto in lista_produtos 
    if all(titulo not in produto['titulo'].split()
    for titulo in eliminar)
]

print("="*100)
for i, produto in enumerate(lista_filtrada, start=1):
    print(f"{i}. {produto['titulo']} | R${produto['price']}")
print("="*100)

df = pd.DataFrame(lista_filtrada)
df.to_csv('./dados.csv', sep=',', encoding='utf-8')