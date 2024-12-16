# 1o EXEMPLO: Ciclo de contagem (gama de valores)
print("1o EXEMPLO: Ciclo de contagem (gama de valores)")

# sum(range(5_000_001))

soma = 0
i = 1
while i <= 5:
    soma += i
    i += 1
print(f"Soma: {soma}")
print(f"Último valor de i: {i}")

# 2o EXEMPLO: Percorrer os elementos de uma estrutura de dados (string)
print("2o EXEMPLO: Percorrer os elementos de uma estrutura de dados (string)")
nome = 'ALBERTO'

i = 0
while i < len(nome):
    print(nome[i])
    i += 1

print('-----------')

i = 0
while i < len(nome):
    print(f"{i} -> {nome[i]}")
    i += 1

print('-----------')

i = len(nome) - 1
while i > -1:
    print(nome[i])
    i -= 1

# 3o EXEMPLO: Percorrer os elementos de uma estrutura de dados (lista)
print("3o EXEMPLO: Percorrer os elementos de uma estrutura de dados (lista)")
vals = [10, -50, 40, -29]

i = 0
soma = 0
while i < len(vals):
    soma += vals[i]
    i += 1

print(f"Soma dos valores da lista {soma}")

# 4o EXEMPLO: Ciclo de validação
print("4o EXEMPLO: Ciclo de validação")

idade_str = input("Idade? ")
while not idade_str.isdigit():
    print("Idade inválida")
    idade_str = input("Idade? ")
print(f"Dobro da idade é {2 * int(idade_str)}")

print('------')

while True:
    idade_str = input("Idade? ")
    if idade_str.isdigit():
        break
    print("Idade inválida")
print(f"Dobro da idade é {2 * int(idade_str)}")

# 5o EXEMPLO: Menu de opções
print("5o EXEMPLO: Menu de opções")

opcao = ''
while opcao != 'T':
    # 1. Exibir o menu de opções
    print("1 - LEVANTAR")
    print("2 - DEPOSITAR")
    print("3 - CONSULTAR SALDO")
    print("T - TERMINAR")
    print()

    # 2. Pedir opção ao utilizador
    opcao = input("Opção: ")

    # 3. Analisar e executar a opção introduzida
    match opcao:
        case '1':
            print("Opção LEVANTAR escolhida")
        case '2':
            print("Opção DEPOSITAR escolhida")
        case '3':
            print("Opção CONSULTAR SALDO escolhida")
        case 'T':
            print("Fim do programa")
        case _:
            print(f"Opção {opcao} inválida")

    # 3. Analisar e executar a opção introduzida (com IF)
    # if opcao == '1':
    #     print("Opção LEVANTAR escolhida")
    # elif opcao == '2':
    #     print("Opção DEPOSITAR escolhida")
    # elif opcao == '3':
    #     print("Opção CONSULTAR SALDO escolhida")
    # elif opcao == 'T':
    #     print("Fim do programa")
    # else:
    #     print(f"Opção {opcao} inválida")

    # 3. Analisar e executar a opção introduzida (com DICIONÁRIOS)
    # def levantar():
    #     print("Opção LEVANTAR escolhida")

    # def depositar():
    #     print("Opção DEPOSITAR escolhida")
    
    # def default():
    #     print(f"Opção {opcao} inválida")

    # accao = {
    #     '1': function(),
    #     '2': depositar,
    # }.get(opcao, default)

    # accao()

    print()
