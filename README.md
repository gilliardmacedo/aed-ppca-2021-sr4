# AED PPCA 2021 - SR4

Nesse repositório estão os arquivos para resolução do problema NP Completo SR4.



O programa principal, com interface gráfica, é o [SR4-InterfaceVisual.py](https://github.com/gilliardmacedo/aed-ppca-2021-sr4/blob/master/SR4-InterfaceVisual.py)


## Soluções

### Força bruta

[SR4-BruteForce.py](https://github.com/gilliardmacedo/aed-ppca-2021-sr4/blob/master/SR4-BruteForce.py)

Esse programa de linha de comando soluciona o problema por força bruta.

### Algoritmo genético com heurística

[SR4-GA-heuristic.py](https://github.com/gilliardmacedo/aed-ppca-2021-sr4/blob/master/SR4-GA-heuristic.py)

Esse programa soluciona o problema através de algoritmo genético que utiliza como função de fitness uma heurística calculada a partir da média esperada de alocação de cada setor.

### Algoritmo genético com função de custo de latência esperado

[SR4-GA-latencyCost.py](https://github.com/gilliardmacedo/aed-ppca-2021-sr4/blob/master/SR4-GA-latencyCost.py)

Esse programa soluciona o problema também com algoritmo genético mas utilizando como função de fitness o próprio custo de latência.
