import string
from random import randint
from time import sleep

from a_star import SimpleGraph, reconstruct_path, a_star_search

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
    "PEPEEEPPPEEEPPEEEPPPEEEPEP",
    "PCEEPEEEEEPPPPPPEEEEEPEECP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPP"]

def criaListaDeArestas(mapa):
    tamanhoY = len(mapa)
    tamanhoX = len(mapa[0])

    print "Iniciando a transformacao de uma matriz " + str(tamanhoX) + " por " + str(tamanhoY) + " em uma lista de arestas\n"

    print "Normalizando baus,escudos e portais em espacos\n"

    for y in xrange(0,tamanhoY):
        mapa[y] = string.replace(mapa[y],"O","E")
        mapa[y] = string.replace(mapa[y],"C","E")
        mapa[y] = string.replace(mapa[y],"S","E")

    print "...Transformando...\n"

    dict = {"Dic":"Dic"}

    for y in xrange(0,tamanhoY):
        for x in xrange(0,tamanhoX):
            if (mapa[y][x]=="E"):
                listConexoes = []
                if (y!=0):
                    if (mapa[y-1][x]=="E"):
                        listConexoes.append(str(y-1)+","+str(x))
                if (y!=tamanhoY-1):
                    if (mapa[y+1][x]=="E"):
                        listConexoes.append(str(y+1)+","+str(x))
                if (x!=0):
                    if (mapa[y][x-1]=="E"):
                        listConexoes.append(str(y)+","+str(x-1))
                if (x!=tamanhoX-1):
                    if (mapa[y][x+1]=="E"):
                        listConexoes.append(str(y)+","+str(x+1))
                dict[str(y)+","+str(x)] = listConexoes
    return dict


#coord eh a coordenada da entidade, uma string "x,y"
#pixX e pixY sao o tamanho x e y do mapa
#blocksX e blocksY sao a quantidade de blocos em cada eixo
#O resultado eh um array com a coordenada em pixel
#do objeto
def getPosition(coord,pixX,pixY, blocksX,blocksY):
    coord = coord.split(",")
    posX = (pixX/blocksX)*float(coord[0])
    posY = (pixY/blocksY)*float(coord[1])
    return [posX,posY]

#posicoes iniciais
posPlayer = [1,3]
posFantasma1 = [15,23]
posFantasma2 = [1,3]
posFantasma3 = [1,5]
posFantasma4 = [1,6]

#retorna a posicao de uma entidade
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
        return posFantasma4

#seta a posicao de uma entidade
#pos eh uma string "x,y"
def setPositionEntidade(entidade, pos):
    if entidade == "Player":
        global posPlayer
        posPlayer = pos
    elif entidade == "Fantasma1":
        global posFantasma1
        posFantasma1 = pos
    elif entidade == "Fantasma2":
        posFantasma2 = pos
    elif entidade == "Fantasma3":
        posFantasma3 = pos
    elif entidade == "Fantasma4":
        posFantasma4 = pos

#currentPos eh a coordenada da entidade, uma string "x,y"
#listOfEdgesDict eh a lista de arestas retornada pela funcao
#criaListaDeArestas(mapa)
def getPossiblePaths(currentPos, listOfEdgesDict):
    if listOfEdgesDict.has_key(currentPos):
        return listOfEdgesDict[currentPos]

listaDeArestas = criaListaDeArestas(mapa)

#SETA QUANTIDADE DE VITORIAS PARA CADA FANTASMA
fant1Vit = 0
fant2Vit = 0
fant3Vit = 0
fant4Vit = 0

#POE O WHILE DENTRO DE UM FOR COM O NUMERO DE VEZES
#QUE VOCE QUER RODAR O EXPERIMENTO

jogando = True

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
    "PEPEEEPPPEEEPPEEEPPPEEEPEP",
    "PCEEPEEEEEPPPPPPEEEEEPEECP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPP"]

for y in xrange(0,len(mapa)):
    mapaPrint[y] = string.replace(mapaPrint[y],"P","#")
    mapaPrint[y] = string.replace(mapaPrint[y],"O","#")
    mapaPrint[y] = string.replace(mapaPrint[y],"X","#")
    mapaPrint[y] = string.replace(mapaPrint[y],"C"," ")
    mapaPrint[y] = string.replace(mapaPrint[y],"S"," ")
    mapaPrint[y] = string.replace(mapaPrint[y],"E"," ")

graph = SimpleGraph()
graph.edges = criaListaDeArestas(mapa)


while(jogando):

    #SETA POSICAO DO JOGADOR E DOS FANTASMAS EM CIMA DO MAPA
    #USA A POSICAO RETORNADA PELO ALGORITMO
    #EXEMPLO: posFantasma1 = algoritmoX.proximoMovimento()
    #Ou algo semelhante. O importante eh calcular qual o proximo movimento
    #e setar aqui
    #eh possivel recuperar a posicao atual com getPositionEntidade()
    #e setar a posical com setPositionEntidade()
    #e possivel pegar as proximas posicoes possiveis com getPossiblePaths()

    #MOSTRA MAPA
    posicaoPlayer = getPositionEntidade("Player")
    posicaoFantasma = getPositionEntidade("Fantasma1")

    # graph = SimpleGraph()
    # graph.edges = criaListaDeArestas(mapa_a_ser_usado)

    linha = list(mapaPrint[posicaoPlayer[0]])
    linha[posPlayer[1]] = "J"
    linha = "".join(linha)
    mapaPrint[posicaoPlayer[0]] = linha

    linhaFantasma = list(mapaPrint[int(posFantasma1[0])])
    linhaFantasma[int(posFantasma1[1])] = "F"
    linhaFantasma = "".join(linhaFantasma)
    mapaPrint[int(posFantasma1[0])] = linhaFantasma


    mapaRun = ""
    for i in mapaPrint:
        mapaRun = mapaRun + i + "\n"
    print mapaRun


    came_from, cost_so_far = a_star_search(graph, str(posicaoFantasma[0])+","+str(posicaoFantasma[1]) ,
                                           str(posicaoPlayer[0])+","+str(posicaoPlayer[1]))

    caminho = reconstruct_path(came_from, str(posicaoFantasma[0])+","+str(posicaoFantasma[1]) , str(posicaoPlayer[0])+","+str(posicaoPlayer[1]))
    print caminho
    #MOSTRA POSICOES NOVAS
    #OU SE QUISER VOCE PODE CRIAR UM MAPA NOVO TEMPORARIO
    #E COLOCAR AS ENTIDADES LA COMO MARCACOES E MOSTRAR
    #GRAFICAMENTE AS POSICOES EM VEZ DE IMPRIMIR

    #TESTA CONDICAO DE VITORIA
    #SE UM OU MAIS DE UM FANTASMA ATINGIRAM
    #O JOGADOR. SETE A CONDICAO DE PARADA
    #E AUMENTE O NUMERO DE VITORIAS DO(S)
    #FANTASMA(S)
    if (posPlayer == posFantasma1):
        fant1Vit+=1
        jogando = False
    if (posPlayer == posFantasma1):
        fant2Vit+=1
        jogando = False
    if (posPlayer == posFantasma1):
        fant3Vit+=1
        jogando = False
    if (posPlayer == posFantasma1):
        fant4Vit+=1
        jogando = False
    if (len(caminho) > 2):
        setPositionEntidade("Fantasma1", caminho[2].split(","))
    else:
        jogando = False

    sleep(0.5)

