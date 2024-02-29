from scraping import Scraping

produtos = Scraping()

print()
url = input('URL Mercado Livre: ')
print()

lista_produtos = produtos.mercado_livre(url)

eliminar = ['Kit', 'Espelho']

lista_filtrada = sorted([
    produto for produto in lista_produtos 
    if all(titulo not in produto['titulo'].split() 
    for titulo in eliminar)], 
    key=lambda x: x['price']
)

print("="*100)
for i, produto in enumerate(lista_filtrada, start=1):
    print(f"{i}. {produto['titulo']} | R${produto['price']}")
print("="*100)

# lista_filtrada = [pessoa for pessoa in lista_de_pessoas if all(nome not in pessoa['nome'].split() for nome in nomes_a_eliminar)]