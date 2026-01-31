total = 0

produtos = {}

for i in range(5):
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    produtos[nome] = preco
    total += preco

print("Valor total da compra:", total)