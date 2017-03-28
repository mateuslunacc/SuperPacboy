import string

posPlayer = [0,0]
posFantasma1 = [0,0]
posFantasma2 = [0,0]
posFantasma3 = [0,0]
posFantasma4 = [0,0]

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
		posPlayer = pos
	elif entidade == "Fantasma1":
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
		

