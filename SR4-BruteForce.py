import itertools
from math import fsum
import time

def carregaR():
    inputMsg = ("Informe as probabilidades de acesso de cada registro em uma linha, separadas por espaços.\n"
    "Lembre-se de que a soma das probabilidades deve ser igual a 1.\n")
    R = list(float(prob) for prob in input(inputMsg).strip().split())
    somaProbability = fsum(R)
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
    d = j - i - 1 if (i < j) else m - i + j - 1
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
        probs.append(R[idx])
    soma = fsum(probs)
    return soma 
    
# Inicio

m = input('Número total de partições (m):\n')
m = int(m)  
k = input('Valor de referência K:\n')
k = int(k)
R = carregaR()
start_time = time.time()

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

todasCombinacoes = []
solucaoAtual = []
indicesJaEscolhidos = []
indicesRestantes = listaIndices.copy()
subconjuntosRestantes = subconjuntos.copy()
obterCombinacoes(todasCombinacoes, m, solucaoAtual, indicesJaEscolhidos,
                 indicesRestantes, subconjuntosRestantes)

print("Encontradas %d possíveis combinações \n" % len(todasCombinacoes))

indicesM = [i for i in range(1, m + 1)]
# Combinacoes simples
possiveisParesEmM = [pair for pair in itertools.combinations(indicesM, 2)]
# Combinações inversas
possiveisParesEmM.extend([(y, x) for (x, y) in possiveisParesEmM])
# Combinaçoes do mesmo indice
possiveisParesEmM.extend([(i, i) for i in indicesM])

custoLatenciaSolucao = 999999
combinacaoSolucao = None
# Cada uma das combinacoes nesse ponto é uma possivel organizacao dos m
# setores, com m listas contendo os indices dos registros na lista/array
# original de entrada do programa. Por exemplo: [[3, 4], [2], [1], [0]]
# indica que o setor 1 está com os itens de indices 3 e 4 da entrada, ou seja,
# o 4o e o 5o item(por causa dos indices em Python começando de zero)
for combinacao in todasCombinacoes:
    custoTotalCombinacao = 0
    indMaiorCustoICombinacao = 0
    indMaiorCustojCombinacao = 0
    
    # Aqui deve ser verificado o custo de latencia dessa combinacao
    # para cada par possivel i e j e acumulado.
    for par in possiveisParesEmM:
        i = par[0]
        j = par[1]
        # Subtrair 1 adequa os indices i e j do problema
        # aos indices de listas em Python
        probI = somarProbabilidades(combinacao[i - 1], R)
        probJ = somarProbabilidades(combinacao[j - 1], R)
        valorIJ = probI * probJ * distancia(i, j, m)
        custoTotalCombinacao += valorIJ
    
    # Verifica se essa combinacao foi a de menor custo entre todas
    if custoTotalCombinacao < custoLatenciaSolucao:
        custoLatenciaSolucao = custoTotalCombinacao
        combinacaoSolucao = combinacao
    
print("\n\n=== Solução ===")
print("Número de registros: %d " % len(R))
print("Disposição dos registros: ")
print(combinacaoSolucao)
print("O custo total de latência dessa solução é %f " % custoLatenciaSolucao)
if custoLatenciaSolucao <= k:
    print("Esse valor é MENOR ou IGUAL a K = %d" % k)
else:
    print("Esse valor é MAIOR que K = %d" % k)
print("--- Tempo de execução: %.4f segundos ---" % (time.time() - start_time))