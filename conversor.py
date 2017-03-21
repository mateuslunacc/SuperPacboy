import string

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

mapaRecebido = [
"PPPPPPPPPXXPPPPPPPPP",
"PPEEEEEEEEEEEEEEEEPP",
"PECPPPEPPPPPPEPPPCEP",
"PEPPSEEEEEEEEEESPPEP",
"PEEPEPPPEPPEPPPEPEEP",
"PPEEEEPEEEEEEPEEEEPP",
"PPPEPEPEPPPPEPEPEPPP",
"OEEEPEPEEEEEEPEPEEEO",
"PPPEPEPPEPPEPPEPEPPP",
"PPEEEEEEEEEEEEEEEEPP",
"PEEPEPPPEPPEPPPEPEEP",
"PEPPEEEEEPPEEEEEPPEP",
"PECPPPEPEPPEPEPPPCEP",
"PPEEEEEPEEEEPEEEEEPP",
"PPPPPPPPPPPPPPPPPPPP"]
	
print criaListaDeArestas(mapaRecebido)
