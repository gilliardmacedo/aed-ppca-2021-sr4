import itertools

def carregaR(n):
    print('Informe a probabilidade de acesso de cada registro em uma linha, separado por espaços.')
    print('Lembre-se de que a soma das probabilidades deve ser igual a 1.')

    Rstring = input()
    Raux = Rstring.split()
    R = []
    somaProbability = 0.0
    for r in Raux:
        R.append(float(r))
        somaProbability = somaProbability + float(r)
    if somaProbability != 1:
        return 'A soma das probabilidades deve ser igual a 1'
    return R


def validaIJ (i, j, m):
    if (j >= 1) & (i >= 1):
        if (j <= m) & (i <= m):
            return True
        else:
            return False
    else:
        return False

def montaSubconjuntos (R):
    lists = []
    for length in range(1, len(R) + 1):
        for subset in itertools.combinations(R, length):
            lists.append(list(subset))
    return lists   

def calculaCustoLatencia (i, j, m):   
    print(i, j, m) 
    varValida = validaIJ (i, j, m)
    if varValida == True:
        if (i < j):
            return (j - i - 1)
        else:
            return (m - i + j - 1)
    else:
        return 'i ou j nao sao validos'
    
def combinar (array, set):   
    return list(combinations(array, set))

# Inicio

m = input('Número total de partições (m):\n')
m = int(m)  
k = input('Valor de referência K:\n')
k = int(k)
n = input('Total de registros(n):\n')
n = int(n)
R = carregaR(n)

# monta subconjunto com os índices dos elementos de R
listaIndices = []
for i in range(len(R)):
    listaIndices.append(i)

# Cria todas as combinações possíveis de todos os tamanhos para os índices
subconjuntos = montaSubconjuntos(listaIndices)

# Dicionario que mapeia os indices aos subconjuntos que o incluem
indiceSubconjuntos = {}
for i in range(len(R)):
    indiceSubconjuntos[i] = []
    for sub in subconjuntos:
        if i in sub:
            indiceSubconjuntos[i].append(sub)

print(indiceSubconjuntos)

# Itera os subconjuntos colocando-os nas partições e para cada solução,
# reduz o problema para as partições restantes



