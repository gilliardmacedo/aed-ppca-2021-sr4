
from itertools import combinations 
def carregaR(n):
    print('Informe, a probabilidade de acesso de cada registro em uma linha, separado por espaços.')
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
    lists = [[]]
    for i in range(len(listaIndices) + 1):
        for j in range(i):
            lists.append(listaIndices[j:i])
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

m = input('Informe o numero total de partições:\n')
m = int(m)  
k = input('Informe o valor de referência k:\n')
k = int(k)
n = input('Informe o numero total de registros:\n')
n = int(n)
R = carregaR(n)

# monta subconjunto com os índices dos elementos de R
listaIndices = []
for i in range(len(R)):
    listaIndices.append(i)
subconjuntos = montaSubconjuntos(listaIndices)

subconjuntosTodasParticoes = []
for i in range(m):
    m = []
    for j in range(len(subconjuntos)):
        m.append(subconjuntos[j])
    subconjuntosTodasParticoes.append({i:m})
    print(subconjuntosTodasParticoes)




Rcontrole = R

print(subconjuntos)



