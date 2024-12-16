"""

for ELEM in COLECÇÃO:
    INST1
    INST2
    ...
    INST_N

ELEM é uma variável
Em Java seria algo semelhante a:
var vals = ArrayList<int>(10);
for(int x : vals) {
     
}
"""

# 1o EXEMPLO: Ciclo de contagem (gama de valores)
print("1o EXEMPLO: Ciclo de contagem (gama de valores)")

soma = 0
for i in range(1, 6):
    soma += i
print(f"Soma: {soma}")
print(f"Último valor de i: {i}")


# 2o EXEMPLO: Percorrer os elementos de uma estrutura de dados (string)
print("2o EXEMPLO: Percorrer os elementos de uma estrutura de dados (string)")
nome = 'ALBERTO'

for letra in nome:
    print(letra)

print('-----------')

for i, letra in enumerate(nome):
    print(f"{i} -> {letra}")

print('-----------')

for letra in reversed(nome):
    print(letra)

# 4o EXEMPLO: Dicionários
print("5o EXEMPLO: Dicionários")
idades = {'alberto': 23, 'ana': 55, 'armando': 19, 'arnaldo': 47}

for nome in idades:   # as chaves são os nomes
    print(nome)

for nome in idades.keys():   # as chaves são os nomes
    print(nome)

for idade in idades.values():
    print(idade)

for nome, idade in idades.items():
    print(nome, idade)
