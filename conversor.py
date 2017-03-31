import string
from random import randint
from time import sleep

import sys

from a_star import SimpleGraph, reconstruct_path, a_star_search
from bfs import bfs
from dfs import find_path

mapa = [
    "PPPPPPPPPPPPXXPPPPPPPPPPPP",
    "PCEEPEEEPPEEEEEEPPEEEPEECP",
    "PEPEEEPEEEEPPPPEEEEPEEEPEP",
    "PEEEPEEPEPEEEEEEPEPEEPEEEP",
    "PPEPPPEPEPEPPPPEPEPEPPPEPP",
    "PPEEPEEEEEEEPPEEEEEEEPEEPP",
    "PPPESEPPPPPEPPEPPPPPESEPPP",
    "PPEEPEEEPEEEPPEEEPEEEPEEPP",
    "OEEPPPPEEEPEEEEPEEEPPPPEEO",
    "PPEEPEEEPEEEPPEEEPEEEPEEPP",
    "PPPEEEPPPPPEEEEPPPPPEEEPPP",
    "PPEEPEEPEEEEPPEEEEPEEPEEPP",
    "PPEPPPEPEPPPPPPPPEPEPPPEPP",
    "PEEEPEEEEEPEEEEPEEEEEPEEEP",
    "PEPEEEPPPEEEPPEPEPPPPPPPPP",
    "PCEEPEEEEEPPPPPPEEEEEEEEEP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPP"]


def criaListaDeArestas(mapa):
    tamanhoY = len(mapa)
    tamanhoX = len(mapa[0])

    print "Iniciando a transformacao de uma matriz " + str(tamanhoX) + " por " + str(
        tamanhoY) + " em uma lista de arestas\n"

    print "Normalizando baus,escudos e portais em espacos\n"

    for y in xrange(0, tamanhoY):
        mapa[y] = string.replace(mapa[y], "O", "E")
        mapa[y] = string.replace(mapa[y], "C", "E")
        mapa[y] = string.replace(mapa[y], "S", "E")

    print "...Transformando...\n"

    dict = {"":""}

    for y in xrange(0, tamanhoY):
        for x in xrange(0, tamanhoX):
            if (mapa[y][x] == "E"):
                listConexoes = []
                if (y != 0):
                    if (mapa[y - 1][x] == "E"):
                        listConexoes.append(str(y - 1) + "," + str(x))
                if (y != tamanhoY - 1):
                    if (mapa[y + 1][x] == "E"):
                        listConexoes.append(str(y + 1) + "," + str(x))
                if (x != 0):
                    if (mapa[y][x - 1] == "E"):
                        listConexoes.append(str(y) + "," + str(x - 1))
                if (x != tamanhoX - 1):
                    if (mapa[y][x + 1] == "E"):
                        listConexoes.append(str(y) + "," + str(x + 1))
                dict[str(y) + "," + str(x)] = listConexoes
    return dict


# coord eh a coordenada da entidade, uma string "x,y"
# pixX e pixY sao o tamanho x e y do mapa
# blocksX e blocksY sao a quantidade de blocos em cada eixo
# O resultado eh um array com a coordenada em pixel
# do objeto
def getPosition(coord, pixX, pixY, blocksX, blocksY):
    coord = coord.split(",")
    posX = (pixX / blocksX) * float(coord[0])
    posY = (pixY / blocksY) * float(coord[1])
    return [posX, posY]

# retorna a posicao de uma entidade
def getPositionEntidade(entidade):
    if entidade == "Player":
        return posPlayer
    elif entidade == "Fantasma1":
        return posFantasma1
    elif entidade == "Fantasma2":
        return posFantasma2
    elif entidade == "Fantasma3":
        return posFantasma3
    elif entidade == "Fantasma4":
        global posFantasma4
        return posFantasma4


# seta a posicao de uma entidade
# pos eh uma string "x,y"
def setPositionEntidade(entidade, pos):
    if entidade == "Player":
        global posPlayer
        posPlayer = pos
    elif entidade == "Fantasma1":
        global posFantasma1
        posFantasma1 = pos
    elif entidade == "Fantasma2":
        global posFantasma2
        posFantasma2 = pos
    elif entidade == "Fantasma3":
        global posFantasma3
        posFantasma3 = pos
    elif entidade == "Fantasma4":
        posFantasma4 = pos


# currentPos eh a coordenada da entidade, uma string "x,y"
# listOfEdgesDict eh a lista de arestas retornada pela funcao
# criaListaDeArestas(mapa)
def getPossiblePaths(currentPos, listOfEdgesDict):
    if listOfEdgesDict.has_key(currentPos):
        return listOfEdgesDict[currentPos]


listaDeArestas = criaListaDeArestas(mapa)

# SETA QUANTIDADE DE VITORIAS PARA CADA FANTASMA
fant1Vit = 0
fant2Vit = 0
fant3Vit = 0
fant4Vit = 0

# POE O WHILE DENTRO DE UM FOR COM O NUMERO DE VEZES
# QUE VOCE QUER RODAR O EXPERIMENTO

jogando = True


def limpa_mapa():
    mapaPrint = [
    "PPPPPPPPPPPPXXPPPPPPPPPPPP",
    "PCEEPEEEPPEEEEEEPPEEEPEECP",
    "PEPEEEPEEEEPPPPEEEEPEEEPEP",
    "PEEEPEEPEPEEEEEEPEPEEPEEEP",
    "PPEPPPEPEPEPPPPEPEPEPPPEPP",
    "PPEEPEEEEEEEPPEEEEEEEPEEPP",
    "PPPESEPPPPPEPPEPPPPPESEPPP",
    "PPEEPEEEPEEEPPEEEPEEEPEEPP",
    "OEEPPPPEEEPEEEEPEEEPPPPEEO",
    "PPEEPEEEPEEEPPEEEPEEEPEEPP",
    "PPPEEEPPPPPEEEEPPPPPEEEPPP",
    "PPEEPEEPEEEEPPEEEEPEEPEEPP",
    "PPEPPPEPEPPPPPPPPEPEPPPEPP",
    "PEEEPEEEEEPEEEEPEEEEEPEEEP",
    "PEPEEEPPPEEEPPEPEPPPPPPPPP",
    "PCEEPEEEEEPPPPPPEEEEEEEEEP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPP"]

    for y in xrange(0, len(mapa)):
        mapaPrint[y] = string.replace(mapaPrint[y], "P", "#")
        mapaPrint[y] = string.replace(mapaPrint[y], "O", " ")
        mapaPrint[y] = string.replace(mapaPrint[y], "X", "#")
        mapaPrint[y] = string.replace(mapaPrint[y], "C", " ")
        mapaPrint[y] = string.replace(mapaPrint[y], "S", " ")
        mapaPrint[y] = string.replace(mapaPrint[y], "E", " ")
    return mapaPrint


graph = SimpleGraph()
graph.edges = criaListaDeArestas(mapa)


def caminho_a_estrela(graph, posicaoFantasma, posicaoPlayer, tie_breaker):

    came_from, lista = a_star_search(graph, str(posicaoFantasma[0]) + "," + str(posicaoFantasma[1]),
                                           str(posicaoPlayer[0]) + "," + str(posicaoPlayer[1]), tie_breaker)

    caminho = reconstruct_path(came_from, str(posicaoFantasma[0]) + "," + str(posicaoFantasma[1]),
                               str(posicaoPlayer[0]) + "," + str(posicaoPlayer[1]))
    caminho = caminho[2:len(caminho)]
    lista = uniquify_list(lista)
    return lista


def caminho_dfs(graph, posicaoFantasma, posicaoPlayer):
    caminho = find_path(graph.edges, str(posicaoFantasma[0]) + "," + str(posicaoFantasma[1]),
                  str(posicaoPlayer[0]) + "," + str(posicaoPlayer[1]), [])
    return caminho[1:len(caminho)]

def caminho_bfs(graph, posicaoFantasma, posicaoPlayer):
    caminho = bfs(graph.edges, str(posicaoFantasma[0]) + "," + str(posicaoFantasma[1]), [])
    return caminho

def uniquify_list(seq, idfun=None):
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

#5 EXPERIMENTOS
for experimentos in range(0, 5):

    #ESCOLHE O ALGORITMO, MELHORAR COMO FAZER ESSA ESCOLHA
    tie_breaker = False

    #coloca o usuario numa posicao random valida
    playerRandom = graph.edges.keys()[randint(0, len(graph.edges.keys()))]
    playerRandomString = playerRandom.split(",")
    playerRandomPosition = [int(playerRandomString[0]), int(playerRandomString[1])]
    setPositionEntidade("Player", playerRandomPosition)

    #coloca o fantasma numa posicao random valida
    for i in range(1,4):
        fantasmaRandom = graph.edges.keys()[randint(0, len(graph.edges.keys()))]
        fantasmaRandomString = fantasmaRandom.split(",")
        fantasmaRandomPosition = [int(fantasmaRandomString[0]), int(fantasmaRandomString[1])]
        setPositionEntidade("Fantasma"+str(i), fantasmaRandomPosition)

    #limpa o mapa para o proximo experimento
    mapaPrint = limpa_mapa()

    print "Player em nova posicao: " + str(playerRandomPosition)
    print "Fantasma em nova posicao: " + str(posFantasma1)
    sleep(5)
    passos = -1


    posicaoPlayer = getPositionEntidade("Player")
    posicaoFantasma1 = getPositionEntidade("Fantasma1")
    posicaoFantasma2 = getPositionEntidade("Fantasma2")
    posicaoFantasma3 = getPositionEntidade("Fantasma3")

    caminhoDFS = caminho_dfs(graph, posicaoFantasma2, posicaoPlayer)

    caminhoBFS = caminho_bfs(graph, posicaoFantasma3, posicaoPlayer)

    caminhoAestrela = caminho_a_estrela(graph, posFantasma1, posicaoPlayer, tie_breaker)

    while (jogando):

        passos += 1

        # TESTA CONDICAO DE VITORIA
        # SE UM OU MAIS DE UM FANTASMA ATINGIRAM
        # O JOGADOR. SETE A CONDICAO DE PARADA
        # E AUMENTE O NUMERO DE VITORIAS DO(S)
        # FANTASMA(S)
        if (posPlayer == posFantasma1):
            vencedor = "A* ganhou"
            fant1Vit += 1
            jogando = False
        if (posPlayer == posFantasma2):
            vencedor = "BFS ganhou"
            fant2Vit += 1
            jogando = False
        if (posPlayer == posFantasma3):
            vencedor = "DFS ganhou"
            fant3Vit += 1
            jogando = False
        if (posPlayer == posFantasma1):
            fant4Vit += 1
            jogando = False
        if (len(caminhoAestrela) <= 0):
            vencedor = "A* ganhou"
        if (len(caminhoDFS) <= 0):
            vencedor = "DSF ganhou"
        if (len(caminhoBFS) <= 0):
            vencedor = "BSF ganhou"
        if (len(caminhoAestrela) > 0) and (len(caminhoBFS) > 0) and (len(caminhoDFS) > 0):
            setPositionEntidade("Fantasma1", caminhoAestrela[0].split(","))
            setPositionEntidade("Fantasma2", [int(caminhoBFS[0].split(",")[0]), int(caminhoBFS[0].split(",")[1])])
            setPositionEntidade("Fantasma3", [int(caminhoDFS[0].split(",")[0]), int(caminhoDFS[0].split(",")[1])])
            caminhoAestrela.pop(0)
            caminhoBFS.pop(0)
            caminhoDFS.pop(0)
        else:
            jogando = False

        # COLOCA O PLAYER E O FANTASMA NO MAPA A SER PRINTADO
        linha = list(mapaPrint[posicaoPlayer[0]])
        linha[posPlayer[1]] = "P"
        linha = "".join(linha)
        mapaPrint[posicaoPlayer[0]] = linha

        linhaFantasma1 = list(mapaPrint[int(posFantasma1[0])])
        linhaFantasma1[int(posFantasma1[1])] = "A"
        linhaFantasma1 = "".join(linhaFantasma1)
        mapaPrint[int(posFantasma1[0])] = linhaFantasma1

        linhaFantasma2 = list(mapaPrint[int(posFantasma2[0])])
        linhaFantasma2[int(posFantasma2[1])] = "B"
        linhaFantasma2 = "".join(linhaFantasma2)
        mapaPrint[int(posFantasma2[0])] = linhaFantasma2

        linhaFantasma3 = list(mapaPrint[int(posFantasma3[0])])
        linhaFantasma3[int(posFantasma3[1])] = "D"
        linhaFantasma3 = "".join(linhaFantasma3)
        mapaPrint[int(posFantasma3[0])] = linhaFantasma3

        #mostra o mapa com a trilha de passos do fantasma
        mapaRun = ""
        for i in mapaPrint:
            mapaRun = mapaRun + i + "\n"
        print mapaRun + "\n\n"

        #printa o caminho baseado na posicao atual do fantasma
        # print caminho

        sleep(.8)

    print "Completou em: %d passos" % passos
    print "Vencedor: %s" % vencedor
    print "\n\n\n"
    jogando = True


