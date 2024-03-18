from scraping import Scraping
import pandas as pd

produtos = Scraping()

def transformar_para_csv(lista):
    eliminar = ['Cabo', 'Espelho', 'Mostruario', 'Mostruário', 'Nf', 'nf', 'Fiscal', 'Entrega', 'Usado', 'Desconto', 'Peças', 'Kit', 'Garantia', 'Nfe', 'Nf-e']

    lista_filtrada = [
        produto for produto in lista 
        if all(titulo not in produto['titulo'].split()
        for titulo in eliminar)
    ]

    print("="*100)
    for i, produto in enumerate(lista_filtrada, start=1):
        print(f"{i}. {produto['titulo']} | R${produto['price']}")
    print("="*100)

    df = pd.DataFrame(lista_filtrada)
    df.to_csv('./dados.csv', sep=',', encoding='utf-8')

print()

while True:
    opcao = input('Qual Marketplace? \n(1) MercadoLivre \n(2) Magalu \n(3) Kabum \n >> ')
    if opcao == "1":
        url = input('Enter the URL: ')
        lista_produtos = produtos.get_mlbr(url)
        transformar_para_csv(lista_produtos)
        break
    if opcao == "2":
        url = input('Enter the URL: ')
        lista_produtos = produtos.get_mglu(url)
        transformar_para_csv(lista_produtos)
        break
    if opcao == "3":
        url = input('Enter the URL: ')
        lista_produtos = produtos.get_kbm(url)
        transformar_para_csv(lista_produtos)
        break
    else:
        print("Inválido.")

