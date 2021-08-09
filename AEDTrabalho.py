
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

def calculaCustoLatencia ( i, j, m):   
    print(i, j, m) 
    varValida = validaIJ (i, j, m)
    if varValida == True:
        if (i < j):
            return (j - i - 1)
        else:
            return (m - i + j - 1)
    else:
        return 'i ou j nao sao validos'

k = input('Informe o valor de referência k:\n')
k = int(k)
n = input('Informe o numero total de registros:\n')
n = int(n)
R = carregaR(n)

print(R)



