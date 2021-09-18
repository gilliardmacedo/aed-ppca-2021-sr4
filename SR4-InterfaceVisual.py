#!/usr/bin/python
# coding: utf-8

# Implementando o menu do sistema "aSR4" que se trata da 
# análise NP-Completo SR4: Custo de Recuperação Esperado
###########
# Imports
###########
import math
import time
import random
import itertools
import itertools
from math import fsum
import time
import sys
from tkinter import BooleanVar, Text
from tkinter.constants import END, FALSE
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from tkinter.ttk import *



############
# Sistema
############

# Declaração de classes
class Sistema:
    
    #Função que representa o encapsulamento da solução do "Algoritmo Exato"
    def algoritmoExato(self):

        # Declaração de Funções
        def carregaR():
            R = list(float(prob) for prob in probabilidades.get().strip().split())
            somaProbability = fsum(R)
            if somaProbability != 1:
                saidasAlgoritmoExatoSomaInvalidaProbabilidades.set("A soma das probabilidades deve ser igual a 1") 
                self.labelSaidasAlgoritmoExatoSomaInvalidaProbabilidades = Label(janela, textvariable=saidasAlgoritmoExatoSomaInvalidaProbabilidades)                
                self.labelSaidasAlgoritmoExatoSomaInvalidaProbabilidades.place(x = 40, y = 180)                               
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
                saidasAlgoritmoExatoValoresInvalidosIeJ.set("Os valores %d e %d para i e j não são válidos" % (i, j))
                self.labelSaidasAlgoritmoExatoValoresInvalidosIeJ = Label(janela, textvariable=saidasAlgoritmoExatoValoresInvalidosIeJ)
                self.labelSaidasAlgoritmoExatoValoresInvalidosIeJ.place(x = 40, y = 200)
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
        
        #Garantir que a tela não fique poluída com informações de execuções passadas
        self.limparLabelsExecucao()
        
        #Captura a entrada de dados realizada pelo usuário do sistema
        m = numTotParticoes.get()
        m = int(m)  
        k = valorReferencia.get()
        k = int(k)
        R = carregaR()

        start_time = time.time()

        # Monta subconjunto com os índices dos elementos de R
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

        self.labelSaidasAlgoritmoExatoPossiveisCombinacoes = Label(janela, text = "Encontradas %d possíveis combinações \n" % len(todasCombinacoes))
        self.labelSaidasAlgoritmoExatoPossiveisCombinacoes.place(x = 40, y = 180)
        
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
        
        # Registra a execução do algoritmo exato
        algoritmoExatoExecutado.set(True)

        # O bloco abaixo é responsável por exibir a respota da execução do algoritmo exato
        self.labelSaidasAlgoritmoExatoSolucao = Label(janela, text = "=== Solução Ótima ===")
        self.labelSaidasAlgoritmoExatoSolucao.place(x = 40, y = 220)
        self.labelSaidasAlgoritmoExatoNumRegistros = Label(janela, text = "Número de registros: %d " % len(R))
        self.labelSaidasAlgoritmoExatoNumRegistros.place(x = 40, y = 240)
        self.labelSaidasAlgoritmoExatoDispRegistros = Label(janela, text = "Disposição dos registros: ")
        self.labelSaidasAlgoritmoExatoDispRegistros.place(x = 40, y = 260)
        self.labelSaidasAlgoritmoExatoCombSolucao = Label(janela, text = combinacaoSolucao)
        self.labelSaidasAlgoritmoExatoCombSolucao.place(x = 175, y = 260)
        self.labelSaidasAlgoritmoExatoCustoLatencia = Label(janela, text = "O custo total de latência dessa solução é %f " % custoLatenciaSolucao)
        self.labelSaidasAlgoritmoExatoCustoLatencia.place(x = 40, y = 280)
        if custoLatenciaSolucao <= k:
            self.labelSaidasAlgoritmoExatoValorK = Label(janela, text = "Esse valor é MENOR ou IGUAL a K = %d" % k)
            self.labelSaidasAlgoritmoExatoValorK.place(x = 40, y = 300)
        else:
            self.labelSaidasAlgoritmoExatoValorK = Label(janela, text = "Esse valor é MAIOR que K = %d" % k)
            self.labelSaidasAlgoritmoExatoValorK.place(x = 40, y = 300)
        self.labelSaidasAlgoritmoExatoTempoExecucao = Label(janela, text = "Tempo de execução: %s segundos" % (time.time() - start_time))
        self.labelSaidasAlgoritmoExatoTempoExecucao.place(x = 40, y = 320)

    #Função que representa o encapsulamento da solução do "Algoritmo Genético"
    def algoritmoGenetico(self):
        # Parâmetros
        NUM_GERACOES = 50
        TAMANHO_POPULACAO = 30
        TAMANHO_SELECAO = 6
        TAMANHO_CROSSOVER = 24

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
            R = list(float(prob) for prob in probabilidades.get().strip().split())
            somaProbability = math.fsum(R)
            if somaProbability != 1:
                saidasAlgoritmoGeneticoSomaInvalidaProbabilidades.set("A soma das probabilidades deve ser igual a 1") 
                self.labelSaidasAlgoritmoGeneticoSomaInvalidaProbabilidades = Label(janela, textvariable=saidasAlgoritmoGeneticoSomaInvalidaProbabilidades)                
                self.labelSaidasAlgoritmoGeneticoSomaInvalidaProbabilidades.place(x = 40, y = 180)                               
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

        def mutacao(particao):
            variavel = 1

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
        
        #Garantir que a tela não fique poluída com informações de execuções passadas
        self.limparLabelsExecucao()

        #Captura a entrada de dados realizada pelo usuário do sistema
        m = numTotParticoes.get()
        m = int(m)  
        k = valorReferencia.get()
        k = int(k)
        R = carregaR()

        start_time = time.time()

        media = 1 / m

        populacao = populacaoInicial(len(R), m, TAMANHO_POPULACAO)

        for geracao in range(NUM_GERACOES):
            scores = [erroParticao(populacao[i], R, media) for i in range(len(populacao))]
            indicesOrdenados = obterIndicesProxGeracao(scores)
            novaPopulacao = [populacao[i][:] for i in indicesOrdenados]
            paresCrossover = obterParesCrossover(indicesOrdenados)
            for par in paresCrossover:
                i = par[0]
                j = par[1]
                novaPopulacao.append(crossover(populacao[i][:], populacao[j][:], R, media))
            for particao in novaPopulacao:
                mutacao(particao)
            populacao = novaPopulacao[:]

        scores = [erroParticao(populacao[i], R, media) for i in range(len(populacao))]
        idxSolucao = scores.index(min(scores))
        individuo = populacao[idxSolucao]
        solucao = solucaoPrintavel(individuo)
        custoLatenciaSolucao = calcularCustoLatencia(R, m, solucao)    

        # Registra a execução do algoritmo exato
        algoritmoGeneticoExecutado.set(True)

        # O bloco abaixo é responsável por exibir a respota da execução do algoritmo exato
        self.labelSaidasAlgoritmoGeneticoSolucao = Label(janela, text = "=== Solução Aproximada ===")
        self.labelSaidasAlgoritmoGeneticoSolucao.place(x = 40, y = 220)
        self.labelSaidasAlgoritmoGeneticoNumRegistros = Label(janela, text = "Número de registros: %d " % len(R))
        self.labelSaidasAlgoritmoGeneticoNumRegistros.place(x = 40, y = 240)
        self.labelSaidasAlgoritmoGeneticoDispRegistros = Label(janela, text = "Disposição dos registros: ")
        self.labelSaidasAlgoritmoGeneticoDispRegistros.place(x = 40, y = 260)
        self.labelSaidasAlgoritmoGeneticoCombSolucao = Label(janela, text = solucao)
        self.labelSaidasAlgoritmoGeneticoCombSolucao.place(x = 175, y = 260)
        self.labelSaidasAlgoritmoGeneticoCustoLatencia = Label(janela, text = "O custo total de latência dessa solução é %f " % custoLatenciaSolucao)
        self.labelSaidasAlgoritmoGeneticoCustoLatencia.place(x = 40, y = 280)
        if custoLatenciaSolucao <= k:
            self.labelSaidasAlgoritmoGeneticoValorK = Label(janela, text = "Esse valor é MENOR ou IGUAL a K = %d" % k)
            self.labelSaidasAlgoritmoGeneticoValorK.place(x = 40, y = 300)
        else:
            self.labelSaidasAlgoritmoGeneticoValorK = Label(janela, text = "Esse valor é MAIOR que K = %d" % k)
            self.labelSaidasAlgoritmoGeneticoValorK.place(x = 40, y = 300)
        self.labelSaidasAlgoritmoGeneticoTempoExecucao = Label(janela, text = "Tempo de execução: %s segundos" % (time.time() - start_time))
        self.labelSaidasAlgoritmoGeneticoTempoExecucao.place(x = 40, y = 320)
  
    #Função para limpar a tela com os parâmetros e resultados da execução do Algoritmo Exato
    def limparExecucao(self):
        if (algoritmoExatoExecutado.get() 
            or saidasAlgoritmoExatoSomaInvalidaProbabilidades.get() != "" 
            or saidasAlgoritmoExatoValoresInvalidosIeJ.get() != ""
            or numTotParticoes.get() != "" 
            or valorReferencia.get() != ""
            or probabilidades.get() != ""):
            self.EntradaNumeroTotalParticoes.delete(0,"end")
            self.EntradaValorReferencia.delete(0,"end")
            self.EntradaProbabilidades.delete(0,"end")
            self.limparLabelsExecucao()
        elif (algoritmoGeneticoExecutado.get() 
            or saidasAlgoritmoGeneticoSomaInvalidaProbabilidades.get() != "" 
            or saidasAlgoritmoGeneticoValoresInvalidosIeJ.get() != ""
            or numTotParticoes.get() != "" 
            or valorReferencia.get() != ""
            or probabilidades.get() != ""):
            self.EntradaNumeroTotalParticoes.delete(0,"end")
            self.EntradaValorReferencia.delete(0,"end")
            self.EntradaProbabilidades.delete(0,"end")
            self.limparLabelsExecucao()


    #Função para limpar a tela retirando os widgets de entrada e limpando os labels
    def limparTela(self):
        if (telaAlgoritmoExatoVisitada.get()):
            self.labelTituloAlgoritmoExato.config(text="")            
            self.labelNumTotParticoes.config(text="")           
            self.EntradaNumeroTotalParticoes.delete(0,"end")           
            self.EntradaNumeroTotalParticoes.destroy()
            self.labelValorReferencia.config(text="")            
            self.EntradaValorReferencia.delete(0,"end")            
            self.EntradaValorReferencia.destroy()
            self.labelProbabilidades.config(text="")            
            self.EntradaProbabilidades.delete(0,"end")
            self.EntradaProbabilidades.destroy()
            self.labelLegendaProbabilidades.config(text="")
            self.botaoExecutar.destroy()
            self.botaoLimpar.destroy()
            self.limparLabelsExecucao()
        elif (telaAlgoritmoGeneticoVisitada.get()):
            self.labelTituloAlgoritmoGenetico.config(text="")
            self.labelNumTotParticoes.config(text="")            
            self.EntradaNumeroTotalParticoes.delete(0,"end") 
            self.EntradaNumeroTotalParticoes.destroy()
            self.labelValorReferencia.config(text="")            
            self.EntradaValorReferencia.delete(0,"end")
            self.EntradaValorReferencia.destroy()
            self.labelProbabilidades.config(text="")            
            self.EntradaProbabilidades.delete(0,"end")
            self.EntradaProbabilidades.destroy()
            self.labelLegendaProbabilidades.config(text="")
            self.botaoExecutar.destroy()
            self.botaoLimpar.destroy()
            self.limparLabelsExecucao()
        elif (telaTodoVisitada.get()):
            self.labelTodo.config(text="")
        elif (telaDescricaoProblemaVisitada.get()):
            self.labelTituloDescricaoProblema.config(text="")
            self.labelDescricaoProblema.config(text="")
        elif (telaSobreVisitada.get()):
            self.labelTituloSobre.config(text="")
            self.labelSobre.config(text="")            

    #Função para limpar os labels existentes na tela
    def limparLabelsExecucao(self):
        if (saidasAlgoritmoExatoSomaInvalidaProbabilidades.get() != ""):            
            saidasAlgoritmoExatoSomaInvalidaProbabilidades.set("")
        elif (saidasAlgoritmoExatoValoresInvalidosIeJ.get() != ""):
            saidasAlgoritmoExatoValoresInvalidosIeJ.set("")
        elif (saidasAlgoritmoGeneticoSomaInvalidaProbabilidades.get() != ""):            
            saidasAlgoritmoGeneticoSomaInvalidaProbabilidades.set("")
        elif (saidasAlgoritmoGeneticoValoresInvalidosIeJ.get() != ""):
            saidasAlgoritmoGeneticoValoresInvalidosIeJ.set("")
        if (algoritmoExatoExecutado.get()):
            self.labelSaidasAlgoritmoExatoPossiveisCombinacoes.config(text="")
            self.labelSaidasAlgoritmoExatoSolucao.config(text="")
            self.labelSaidasAlgoritmoExatoNumRegistros.config(text="")
            self.labelSaidasAlgoritmoExatoDispRegistros.config(text="")
            self.labelSaidasAlgoritmoExatoCombSolucao.config(text="")
            self.labelSaidasAlgoritmoExatoCustoLatencia.config(text="")
            self.labelSaidasAlgoritmoExatoValorK.config(text="")
            self.labelSaidasAlgoritmoExatoTempoExecucao.config(text="")
        elif (algoritmoGeneticoExecutado.get()):         
            self.labelSaidasAlgoritmoGeneticoSolucao.config(text="")
            self.labelSaidasAlgoritmoGeneticoNumRegistros.config(text="")
            self.labelSaidasAlgoritmoGeneticoDispRegistros.config(text="")
            self.labelSaidasAlgoritmoGeneticoCombSolucao.config(text="")
            self.labelSaidasAlgoritmoGeneticoCustoLatencia.config(text="")
            self.labelSaidasAlgoritmoGeneticoValorK.config(text="")
            self.labelSaidasAlgoritmoGeneticoTempoExecucao.config(text="")           
    
    # Monta a tela de entrada inicial dos dados relativo ao algoritmo exato
    def telaAlgoritmoExato(self):
        #Limpa a tela antes de montar a tela do Algoritmo Exato
        self.limparTela()

        self.labelTituloAlgoritmoExato = Label(janela, text = "ALGORITMO EXATO")
        self.labelTituloAlgoritmoExato.place(x = 300, y = 10)
        
        # Label da entrada do número total de partições (m) 
        self.labelNumTotParticoes = Label(janela, text = "Número total de partições (m):")
        self.labelNumTotParticoes.place(x = 40, y = 60)
        self.EntradaNumeroTotalParticoes = Entry(janela, textvariable = numTotParticoes, width = 10)
        self.EntradaNumeroTotalParticoes.place(x = 230,y = 60) 
      
        # Label da entrada do valor de referência K
        self.labelValorReferencia = Label(janela, text = "Valor de referência K:")
        self.labelValorReferencia.place(x = 40, y = 100)     
        self.EntradaValorReferencia = Entry(janela, textvariable = valorReferencia, width = 10)
        self.EntradaValorReferencia.place(x = 230, y = 100)

        # Label da entrada do número total de partições (m) 
        self.labelProbabilidades = Label(janela, text = "Probabilidades de acesso a cada registro, separadas por espaços, totalizando 1:")
        self.labelProbabilidades.place(x = 40, y = 140)  
        self.EntradaProbabilidades = Entry(janela, textvariable = probabilidades, width = 30)
        self.EntradaProbabilidades.place(x = 40, y = 160) 

        # Label da legenda das Probabilidades
        self.labelLegendaProbabilidades = Label(janela, text = "Exemplo: 0.3 0.2 0.1 0.4")
        self.labelLegendaProbabilidades.place(x = 230, y = 160)

        # Botão que executa o Algoritmo Exato
        self.botaoExecutar = Button(janela, text = "Executar", command = self.algoritmoExato)
        self.botaoExecutar.place(x = 500, y = 160)

        # Botão que limpa a tela
        self.botaoLimpar = Button(janela, text = "Limpar", command = self.limparExecucao)
        self.botaoLimpar.place(x = 650, y = 160)

        #Registra que a tela do Algoritmo Exato foi visitada
        telaAlgoritmoExatoVisitada.set(True)

        #Apagando todos os registros de atividades realizadas anteriores a esta
        algoritmoGeneticoExecutado.set(False)
        telaAlgoritmoGeneticoVisitada.set(False)
        telaTodoVisitada.set(False)
        telaDescricaoProblemaVisitada.set(False)
        telaSobreVisitada.set(False)

    # Monta a tela de entrada inicial dos dados relativo ao algoritmo genetico
    def telaAlgoritmoGenetico(self):
        #Limpa a tela antes de montar a tela do Algoritmo genetico
        self.limparTela()

        self.labelTituloAlgoritmoGenetico = Label(janela, text = "ALGORITMO GENÉTICO")
        self.labelTituloAlgoritmoGenetico.place(x = 300, y = 10)
        
        # Label da entrada do número total de partições (m) 
        self.labelNumTotParticoes = Label(janela, text = "Número total de partições (m):")
        self.labelNumTotParticoes.place(x = 40, y = 60)
        self.EntradaNumeroTotalParticoes = Entry(janela, textvariable = numTotParticoes, width = 10)
        self.EntradaNumeroTotalParticoes.place(x = 230,y = 60) 
      
        # Label da entrada do valor de referência K
        self.labelValorReferencia = Label(janela, text = "Valor de referência K:")
        self.labelValorReferencia.place(x = 40, y = 100)     
        self.EntradaValorReferencia = Entry(janela, textvariable = valorReferencia, width = 10)
        self.EntradaValorReferencia.place(x = 230, y = 100)

        # Label da entrada do número total de partições (m) 
        self.labelProbabilidades = Label(janela, text = "Probabilidades de acesso a cada registro, separadas por espaços, totalizando 1:")
        self.labelProbabilidades.place(x = 40, y = 140)  
        self.EntradaProbabilidades = Entry(janela, textvariable = probabilidades, width = 30)
        self.EntradaProbabilidades.place(x = 40, y = 160) 

        # Label da legenda das Probabilidades
        self.labelLegendaProbabilidades = Label(janela, text = "Exemplo: 0.3 0.2 0.1 0.4")
        self.labelLegendaProbabilidades.place(x = 230, y = 160)

        # Botão que executa o Algoritmo genetico
        self.botaoExecutar = Button(janela, text = "Executar", command = self.algoritmoGenetico)
        self.botaoExecutar.place(x = 500, y = 160)

        # Botão que limpa a tela
        self.botaoLimpar = Button(janela, text = "Limpar", command = self.limparExecucao)
        self.botaoLimpar.place(x = 650, y = 160)

        #Registra que a tela do Algoritmo genetico foi visitada
        telaAlgoritmoGeneticoVisitada.set(True)

        #Apagando todos os registros de atividades realizadas anteriores a esta                
        algoritmoExatoExecutado.set(False)
        telaAlgoritmoExatoVisitada.set(False)
        telaTodoVisitada.set(False)
        telaDescricaoProblemaVisitada.set(False)
        telaSobreVisitada.set(False)
    
    
    #Função que representa um item de menu que chama algo a implementar
    def todo(self):
        #Limpa a tela antes de montar a tela do "A Implementar"
        self.limparTela()
        
        self.labelTodo = Label(janela,text="[A implementar]")
        self.labelTodo.pack()

        #Registra que a tela "A Implementar" foi visitada
        telaTodoVisitada.set(True)

        #Apagando todos os registros de atividades realizadas anteriores a esta
        telaAlgoritmoExatoVisitada.set(False)
        telaAlgoritmoGeneticoVisitada.set(False)
        algoritmoExatoExecutado.set(False)
        algoritmoGeneticoExecutado.set(False)
        telaDescricaoProblemaVisitada.set(False)
        telaSobreVisitada.set(False)

    #Função que descreve o problema NP-Completo SR4
    def descricaoProblema(self):
        #Limpa a tela antes de montar a tela de Descrição do Problema
        self.limparTela()

        self.labelTituloDescricaoProblema = Label(janela, text = "DESCRIÇÃO DO PROBLEMA NP-COMPLETO SR4")
        self.labelTituloDescricaoProblema.place(x = 270, y = 10)
        descProblema = """    O problema Np-Completo SR4 é assim classificado por ser de complexidade não polinomial em tempo de resolução computacional.\n
    Sua descrição matemática pode ser compreendida da seguinte forma:\n
    Dada uma instância de um conjunto R de registros, a probabilidade racional p(r) pertence a [0; 1] para cada r pertencente a R, com somatório\n
    das probabilidades totalizando 1, número m de setores, e um inteiro positivo K.\n
    Pergunta: Há uma partição de R em subconjuntos disjuntos R1; R2; ..., Rm de modo que, se p(Ri) representa o somatório das probabilidades\n 
    e o "custo de latência" d(i,j) seja definido como j - i - 1 se 1 <= i < j <= m e ser m - i + j - 1 se 1 <= j <= i <= m, então a soma que se\n 
    sobrepõe a todos os pares ordenados i, j, 1 <= i, j <= m, de p(Ri) * p(Rj) * d(i; j) é no máximo K?\n
    Referência: [Cody e Coffman, 1976]. Transformação da partição, 3 partições.\n
    Comentário: NP-completo no sentido forte. NP-completo e solucionável em tempo pseudo-polinomial para cada m >= 2 fixo."""
        self.labelDescricaoProblema = Label(janela, text=descProblema)
        self.labelDescricaoProblema.place(x=15, y = 30)
        
        #Registra que a tela de Descrição do Problema foi visitada
        telaDescricaoProblemaVisitada.set(True)

        #Apagando todos os registros de atividades realizadas anteriores a esta
        telaAlgoritmoExatoVisitada.set(False)
        telaAlgoritmoGeneticoVisitada.set(False)
        algoritmoExatoExecutado.set(False)
        algoritmoGeneticoExecutado.set(False)
        telaTodoVisitada.set(False)
        telaSobreVisitada.set(False)
        

    #Função que apresenta a disciplina, o professor e os integrantes do grupo 5 (tema SR4)
    def sobre(self):
        #Limpa a tela antes de montar a tela sobre os autores e orientador
        self.limparTela()

        self.labelTituloSobre = Label(janela, text = "AUTORES E ORIENTADOR")
        self.labelTituloSobre.place(x = 320, y = 10)
        autores = """    Gilliard Macedo Vieira de Carvalho\n
    E-mail: gilliardmacedo@gmail.com\n\n
    Luís Augusto Vieira Ribeiro\n
    E-mail: lavribeiro@gmail.com\n\n
    Stella Mendes Meireles Bonifácio\n 
    E-mail: stellameireles@gmail.com\n\n\n
    Orientador: Edison Ishikawa\n
    E-mail: ishikawa@unb.br\n\n\n
    Programa de Pós-Graduação em Computação Aplicada\n
    Universidade de Brasília - UnB\n
    Brasília, Brasil"""
        self.labelSobre = Label(janela, text=autores)
        self.labelSobre.place(x=280, y = 30)

        #Registra que a tela de Descrição do Problema foi visitada
        telaSobreVisitada.set(True)

        #Apagando todos os registros de atividades realizadas anteriores a esta
        telaAlgoritmoExatoVisitada.set(False)
        telaAlgoritmoGeneticoVisitada.set(False)
        telaDescricaoProblemaVisitada.set(False)
        telaTodoVisitada.set(False)
    
    #Monta a interface gráfica do sistema aSR4
    def __init__(self, janela):
      
        # Instruções
        lblTitle=Label(janela, text="Problema SR4", font=("Helvetica", 48))
        lblTitle.place(x=230, y=50)
        
        lblInst=Label(janela, text="Selecione na barra de menu a opção desejada", font=("Helvetica", 24))
        lblInst.place(x=150, y=400)
        
        #Título da janela
        janela.title("Análise NP-Completo SR4: Custo de Recuperação Esperado")
        
        #Tamanho da janela
        janela.geometry('800x600')

        #Construindo o Menu do sistema
        barraMenu = tk.Menu(janela)
        menuASR4 = tk.Menu(barraMenu, tearoff=0)
        subMenuASR4 = tk.Menu(barraMenu, tearoff=0)
        itensSubMenuASR4= tk.Menu(barraMenu, tearoff=0)
        itensSubMenuASR4.add_cascade()
        menuASR4.add_command(label="Algoritmo Exato", command=self.telaAlgoritmoExato)
        menuASR4.add_command(label="Algoritmo Genético", command=self.telaAlgoritmoGenetico)
        menuASR4.add_separator()
        menuASR4.add_command(label="Sair", command=quit)
        barraMenu.add_cascade(label="Início", menu=menuASR4)
        
        menuAjuda = tk.Menu(barraMenu, tearoff=0)        
        menuAjuda.add_command(label="Descrição do Problema", command=self.descricaoProblema)
        menuAjuda.add_command(label="Sobre", command=self.sobre)
        barraMenu.add_cascade(label="Ajuda", menu=menuAjuda)

        janela.config(menu=barraMenu)
        janela.mainloop()

#########################
# Programa Principal
#########################
if __name__ == "__main__":
    
    #Janela do sistema aSR4
    janela = tk.Tk()
    
    #Declaração de variáveis globais        
    numTotParticoes = tk.StringVar()
    valorReferencia = tk.StringVar()
    probabilidades = tk.StringVar()
    saidasAlgoritmoExatoSomaInvalidaProbabilidades = tk.StringVar()
    saidasAlgoritmoGeneticoSomaInvalidaProbabilidades = tk.StringVar()
    saidasAlgoritmoExatoValoresInvalidosIeJ = tk.StringVar()
    saidasAlgoritmoGeneticoValoresInvalidosIeJ = tk.StringVar()
    algoritmoExatoExecutado = tk.BooleanVar(False)
    algoritmoGeneticoExecutado = tk.BooleanVar(False)
    telaAlgoritmoExatoVisitada = tk.BooleanVar(False)
    telaAlgoritmoGeneticoVisitada = tk.BooleanVar(False)
    telaDescricaoProblemaVisitada = tk.BooleanVar(False)
    telaSobreVisitada = tk.BooleanVar(False)
    telaTodoVisitada = tk.BooleanVar(False)

    #Chamando o sistema
    Sistema(janela)    