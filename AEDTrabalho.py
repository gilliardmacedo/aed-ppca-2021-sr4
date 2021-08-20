import itertools
from math import fsum

def carregaR():
    inputMsg = ("Informe as probabilidades de acesso de cada registro em uma linha, separadas por espaços.\n"
    "Lembre-se de que a soma das probabilidades deve ser igual a 1.\n")
    R = list(float(prob) for prob in input(inputMsg).strip().split())
    somaProbability = sum(R)
    if somaProbability != 1:
        raise ValueError("A soma das probabilidades deve ser igual a 1")
    return R

def validaIJ (i, j, m):
    return j >= 1 and i >= 1 and j <= m and i <= m

def montaSubconjuntos (R):
    lists = []
    for length in range(1, len(R) + 1):
        for subset in itertools.combinations(R, length):
            lists.append(list(subset))
    return lists   

def distancia (i, j, m):
    if not validaIJ(i, j, m):
        raise ValueError("Os valores %d e %d para i e j não são válidos" % (i, j))
    diff = j - i - 1
    d = diff if (i < j) else m + diff
    print("Distancia %d , %d = %d" % (i, j, d))
    return d

def filtrarSubconjuntosRestantes(subconjuntosTotais, subconjuntoEscolhido):
    retorno = []
    for sub in subconjuntosTotais:
        possuiAlgumItem = False
        for item in sub:
            if item in subconjuntoEscolhido:
                possuiAlgumItem = True
                break
        if not possuiAlgumItem:
            retorno.append(sub)
    return retorno

# Itera os subconjuntos colocando-os nas partições e para cada solução,
# reduz o problema para as partições restantes
def obterCombinacoes(todasCombinacoes, numSetores, solucaoAtual, idxEscolhidos, idxRestantes, cnjRestantes):
    # Encontrou solução
    if len(solucaoAtual) == numSetores and not cnjRestantes:
        todasCombinacoes.append(solucaoAtual)
    # Não consegue mais criar soluções a partir desse ponto
    elif (len(solucaoAtual) == numSetores and cnjRestantes) or not cnjRestantes:
        return
    # Prosseguir montando soluçao
    else:
        for conjuntoAtual in cnjRestantes:
            novaSolucao = solucaoAtual.copy()
            novaSolucao.append(conjuntoAtual)
            novoIdxEscolhidos = indicesJaEscolhidos.copy()
            novoIdxEscolhidos.extend(sub)
            novoIdxRestantes = list(set(idxRestantes) - set(novoIdxEscolhidos))
            novoCnjRestantes = filtrarSubconjuntosRestantes(cnjRestantes, conjuntoAtual)
            obterCombinacoes(todasCombinacoes, numSetores, novaSolucao, novoIdxEscolhidos, novoIdxRestantes, novoCnjRestantes)

def somarProbabilidades(indices, R):
    probs = []
    for idx in indices:
        print("R[idx]: %f" % R[idx])
        probs.append(R[idx])
    soma = fsum(probs)
    print("Soma dos indices: %f " % soma)
    print(indices)
    print(R)
    return soma 
    
# Inicio

m = input('Número total de partições (m):\n')
m = int(m)  
k = input('Valor de referência K:\n')
k = int(k)
R = carregaR()

# monta subconjunto com os índices dos elementos de R
listaIndices = [i for i in range(len(R))]

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

todasCombinacoes = []
solucaoAtual = []
indicesJaEscolhidos = []
indicesRestantes = listaIndices.copy()
subconjuntosRestantes = subconjuntos.copy()
obterCombinacoes(todasCombinacoes, m, solucaoAtual, indicesJaEscolhidos,
                 indicesRestantes, subconjuntosRestantes)

print("Encontradas %d possíveis combinações" % len(todasCombinacoes))

indicesM = [i for i in range(1, m + 1)]
possiveisParesEmM = [pair for pair in itertools.combinations(indicesM, 2)]

maiorCustoLatencia = -1
indMaiorCustoI = 0
indMaiorCustoj = 0
combinacaoSolucao = None
# Cada uma das combinacoes nesse ponto é uma possivel organizacao dos m
# setores, com m listas contendo os indices dos registros na lista/array
# original de entrada do programa. Por exemplo: [[3, 4], [2], [1], [0]]
# indica que o setor 1 está com os itens de indices 3 e 4 da entrada, ou seja,
# o 4o e o 5o item(por causa dos indices em Python começando de zero)
for combinacao in todasCombinacoes:
    print("== Combinacao ==")
    print(combinacao)
    # Aqui deve ser verificado o custo de latencia dessa combinacao
    # para cada par possivel i e j.
    for par in possiveisParesEmM:
        i = par[0]
        j = par[1]
        print("i: %d, j: %d" % (i, j))
        # Subtrair 1 adequa os indices i e j do problema
        # aos indices de listas em Python
        probI = somarProbabilidades(combinacao[i - 1], R)
        probJ = somarProbabilidades(combinacao[j - 1], R)
        print("probI: %f " % probI)
        print("probJ: %f " % probJ)
        print("d(i,j): %d " % distancia(i, j, m))
        print("d(j,i): %d " % distancia(j, i, m))
        valorIJ = probI * probJ * distancia(i, j, m)
        valorJI = probI * probJ * distancia(j, i, m)
        print("Valor i,j: %f " % valorIJ)
        print("Valor j,i: %f " % valorJI)
        if valorIJ > maiorCustoLatencia:
            maiorCustoLatencia = valorIJ
            indMaiorCustoI = i
            indMaiorCustoJ = j
            combinacaoSolucao = combinacao
        if valorJI > maiorCustoLatencia:
            maiorCustoLatencia = valorJI
            indMaiorCustoI = j
            indMaiorCustoJ = i
            combinacaoSolucao = combinacao
            
print("O maior custo de latência encontrado foi %f " % maiorCustoLatencia)
print("Disposição dos registros: ")
print(combinacaoSolucao)
print("O valor foi encontrado para i = %d e j = %d" % (indMaiorCustoI, indMaiorCustoJ))