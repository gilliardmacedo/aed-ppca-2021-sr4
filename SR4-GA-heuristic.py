# Implementação de algoritmo genético para solução do SR4
# utilizando o cálculo exato como teste

import math
import time
import random
import itertools

# Parâmetros
NUM_GERACOES = 50
TAMANHO_POPULACAO = 30
TAMANHO_SELECAO = 6
TAMANHO_CROSSOVER = 24
PROBABILIDADE_MUTACAO = 0.1
NUM_STEPS_MUTACAO_REMANESCENTES = 2
NUM_STEPS_MUTACAO_CROSSOVER = 3

# População inicial
def populacaoInicial(n, m, tamanhoPop):
    populacao = []
    for _ in range(tamanhoPop):
        individuos = [[0 for i in range(n)] for i in range(m)]
        for i in range(n):
            individuoComItem = random.choice(individuos)
            individuoComItem[i] = 1
        populacao.append(individuos)
    return populacao

def carregaR():
    inputMsg = ("Informe as probabilidades de acesso de cada registro em uma linha, separadas por espaços.\n"
    "Lembre-se de que a soma das probabilidades deve ser igual a 1.\n")
    R = list(float(prob) for prob in input(inputMsg).strip().split())
    somaProbability = math.fsum(R)
    if somaProbability != 1:
        raise ValueError("A soma das probabilidades deve ser igual a 1")
    return R

def somaSetor(setor, R):
    probs = []
    for i in range(len(setor)):
        if setor[i] == 1:
            probs.append(R[i])
    return math.fsum(probs)

def erroSetor(setor, R, media):
    return abs(somaSetor(setor, R) - media)
    
def erroParticao(particao, R, media):
    quadradosDosErros = []
    for setor in particao:
        quadradosDosErros.append(pow(erroSetor(setor, R, media), 2))
    somaDosQuadrados = math.fsum(quadradosDosErros)
    return math.sqrt(somaDosQuadrados)

def obterIndicesProxGeracao(scores):
    indicesOrdenados = [i for i in range(len(scores))]
    indicesOrdenados = sorted(indicesOrdenados, key = lambda idx: scores[idx])
    return indicesOrdenados[:TAMANHO_SELECAO]

def obterParesCrossover(indices):
    possiveisPares = [pair for pair in itertools.combinations(indices, 2)]
    random.shuffle(possiveisPares)
    return possiveisPares[:TAMANHO_CROSSOVER]

def obterMenorSetorAtual(somasSetores):
    return somasSetores.index(min(somasSetores))
    
def tratarResultado(particao, R):
    valoresPresentes = [0 for i in range(len(R))]
    # Remove duplicados
    for i in range(len(particao)):
        setor = particao[i]
        for j in range(len(setor)):
            if valoresPresentes[j] == 1 and setor[j] == 1:
                setor[j] = 0
            elif valoresPresentes[j] == 0 and setor[j] == 1:
                valoresPresentes[j] = 1
    # Inclui restantes
    # Prioriza por item de maior prioridade
    indicesRestantes = [index for index, value in enumerate(valoresPresentes) if value == 0]
    indicesRestantes = sorted(indicesRestantes, key = lambda idx: R[idx], reverse=True)
    for i in indicesRestantes:
        # Inclui no menor conjunto
        probabilidades = printProbabilidades(particao, R)
        somasSetores = [math.fsum(probabilidades[i]) for i in range(len(probabilidades))]
        menorSetor = obterMenorSetorAtual(somasSetores)
        particao[menorSetor][i] = 1
            
    
def crossover(particaoI, particaoJ, R, media):
    scoresI = [erroSetor(particaoI[i], R, media) for i in range(len(particaoI))]
    scoresJ = [erroSetor(particaoJ[j], R, media) for j in range(len(particaoJ))]
    indicesOrdenadosI = [i for i in range(len(scoresI))]
    indicesOrdenadosI = sorted(indicesOrdenadosI, key = lambda idx: scoresI[idx])
    indicesOrdenadosJ = [i for i in range(len(scoresJ))]
    indicesOrdenadosJ = sorted(indicesOrdenadosJ, key = lambda idx: scoresJ[idx])
    idxI = 0
    idxJ = 0
    totalSetores = 0
    resultadoCrossover = []
    while totalSetores < len(scoresI):
        if idxI == len(scoresI):
            if particaoJ[indicesOrdenadosJ[idxJ]] not in resultadoCrossover:
                resultadoCrossover.append(particaoJ[indicesOrdenadosJ[idxJ]][:])
            else:
                resultadoCrossover.append([0 for i in range(len(R))])
            totalSetores = totalSetores + 1
            continue
        elif idxJ == len(scoresJ):
            if particaoI[indicesOrdenadosI[idxI]] not in resultadoCrossover:
                resultadoCrossover.append(particaoI[indicesOrdenadosI[idxI]][:])
            else:
                resultadoCrossover.append([0 for i in range(len(R))])
            totalSetores = totalSetores + 1
            continue
        if scoresI[indicesOrdenadosI[idxI]] <= scoresJ[indicesOrdenadosJ[idxJ]]:
            if particaoI[indicesOrdenadosI[idxI]] not in resultadoCrossover:
                resultadoCrossover.append(particaoI[indicesOrdenadosI[idxI]][:])
                totalSetores = totalSetores + 1
            idxI = idxI + 1
        else:
            if particaoJ[indicesOrdenadosJ[idxJ]] not in resultadoCrossover:
                resultadoCrossover.append(particaoJ[indicesOrdenadosJ[idxJ]][:])
                totalSetores = totalSetores + 1
            idxJ = idxJ + 1
    tratarResultado(resultadoCrossover, R)
    return resultadoCrossover[:]

def mutacao(particao, probabilidade, numSteps):
    for i in range(numSteps):
        if random.random() <= probabilidade:
            setorModificado = random.choice(particao)
            idxModificado = random.randrange(0, len(setorModificado))
            if setorModificado[idxModificado] == 0:
                # troca de 0 pra 1 depois de retirar o 1 do setor que originalmente possuia o registro
                for setor in particao:
                    if setor[idxModificado] == 1:
                        setor[idxModificado] = 0
                setorModificado[idxModificado] = 1
            else:
                # troca de 1 pra 0 e depois atribui o registro a outro setor
                setorModificado[idxModificado] = 0
                novoSetor = random.choice(particao)
                novoSetor[idxModificado] = 1
    

def printProbabilidades(solucao, R):
    setores = []
    for setorSolucao in solucao:
        setores.append([R[index] for index, value in enumerate(setorSolucao) if value == 1])
    return setores
                    
def solucaoPrintavel(solucao):
    setores = []
    for setorSolucao in solucao:
        setores.append([index for index, value in enumerate(setorSolucao) if value == 1])
    return setores

def distancia (i, j, m):
    return j - i - 1 if (i < j) else m - i + j - 1

def somarProbabilidades(indices, R):
    probs = []
    for idx in indices:
        probs.append(R[idx])
    soma = math.fsum(probs)
    return soma

def calcularCustoLatencia(R, m, solucao):
    indicesM = [i for i in range(1, m + 1)]
    # Combinacoes simples
    possiveisParesEmM = [pair for pair in itertools.combinations(indicesM, 2)]
    # Combinações inversas
    possiveisParesEmM.extend([(y, x) for (x, y) in possiveisParesEmM])
    # Combinaçoes do mesmo indice
    possiveisParesEmM.extend([(i, i) for i in indicesM])
    custoTotalCombinacao = 0
    # Aqui deve ser verificado o custo de latencia dessa combinacao
    # para cada par possivel i e j e acumulado.
    for par in possiveisParesEmM:
        i = par[0]
        j = par[1]
        # Subtrair 1 adequa os indices i e j do problema
        # aos indices de listas em Python
        probI = somarProbabilidades(solucao[i - 1], R)
        probJ = somarProbabilidades(solucao[j - 1], R)
        valorIJ = probI * probJ * distancia(i, j, m)
        custoTotalCombinacao += valorIJ
    return custoTotalCombinacao
        

# Inicio
m = input('Número total de partições (m):\n')
m = int(m)  
k = input('Valor de referência K:\n')
k = int(k)
R = carregaR()

start_time = time.time()

media = 1 / m

populacao = populacaoInicial(len(R), m, TAMANHO_POPULACAO)

for geracao in range(NUM_GERACOES):
    scores = [erroParticao(populacao[i], R, media) for i in range(len(populacao))]
    indicesOrdenados = obterIndicesProxGeracao(scores)
    novaPopulacao = [populacao[i][:] for i in indicesOrdenados]
    for solucao in novaPopulacao:
        mutacao(solucao, PROBABILIDADE_MUTACAO, NUM_STEPS_MUTACAO_REMANESCENTES)
    paresCrossover = obterParesCrossover(indicesOrdenados)
    for par in paresCrossover:
        i = par[0]
        j = par[1]
        novoIndividuo = crossover(populacao[i][:], populacao[j][:], R, media)
        mutacao(novoIndividuo, PROBABILIDADE_MUTACAO, NUM_STEPS_MUTACAO_CROSSOVER)
        novaPopulacao.append(novoIndividuo)
    populacao = novaPopulacao[:]

scores = [erroParticao(populacao[i], R, media) for i in range(len(populacao))]
idxSolucao = scores.index(min(scores))
print("Solução")
individuo = populacao[idxSolucao]
solucao = solucaoPrintavel(individuo)
print(solucao)
custoLatenciaSolucao = calcularCustoLatencia(R, m, solucao)
print("O custo total de latência dessa solução é %f " % custoLatenciaSolucao)    

print("--- Tempo de execução: %.4f segundos ---" % (time.time() - start_time))