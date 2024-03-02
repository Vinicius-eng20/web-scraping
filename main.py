from scraping import Scraping
import pandas as pd

produtos = Scraping()

print()
url = input('URL Mercado Livre: ')
print()

lista_produtos = produtos.mercado_livre(url)

eliminar = ['Cabo', 'Placa', 'Mostruario', 'Mostruário', 'Nf', 'nf', 'Fiscal', 'Entrega', 'Usado', 'Desconto', 'Peças', 'Kit', 'Garantia', 'Nfe', 'Nf-e']

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
# lista_filtrada = [pessoa for pessoa in lista_de_pessoas if all(nome not in pessoa['nome'].split() for nome in nomes_a_eliminar)]