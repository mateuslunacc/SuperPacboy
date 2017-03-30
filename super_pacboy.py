#! /usr/bin/env python
# -*- coding: iso-8859-15 -*- 
###	Jogo Super Pacboy ###

import pygame
from pygame.locals import *
import pickle
from base64 import b64encode as encriptar
from base64 import b64decode as desencriptar
from time import time
import string

if not pygame.mixer: print ("Jogo sem som, falta pygame.mixer")

pygame.init()

LARGURA_DA_TELA = 400
ALTURA_DA_TELA = 300
TAMANHO_DA_TELA = (LARGURA_DA_TELA, ALTURA_DA_TELA)
tela = pygame.display.set_mode(TAMANHO_DA_TELA, 0, 32)
pygame.display.set_caption("Super Pacboy")
tempo = pygame.time.Clock()

pygame.mouse.set_visible(False)   #Esconde o ponteiro do mouse dentro da tela

#################################################
####		Carregar Fonte
#################################################

fonte_diretorio = pygame.font.match_font("comicsansms")
texto = pygame.font.Font(fonte_diretorio, 20)
texto_recorde = texto.render("Voce bateu o recorde!", True, (204, 255, 51))	
texto_seu_nome = texto.render("Digite o seu nome:", True, (204, 255, 51))

################################################
####		Carregar Sons
################################################

#Efeitos Sonoros
som_teletransportar = pygame.mixer.Sound("sons/teletransportar.wav")
grito_de_morte = pygame.mixer.Sound("sons/grito_de_morte.wav")
abrir_portao = pygame.mixer.Sound("sons/abrir_portao.wav")
abrir_portao.set_volume(0.1)
pegou_escudo = pygame.mixer.Sound("sons/pegou_escudo.wav")
capturou_bau = pygame.mixer.Sound("sons/capturou_bau.wav")
som_ganhou = pygame.mixer.Sound("sons/som_ganhou.wav")
som_ganhou.set_volume(1)
inimigo_morreu = pygame.mixer.Sound("sons/inimigo_morreu.wav")

###############################################
####		Carregar Sprites
###############################################

pacboy_lado = pygame.image.load("sprites/pacboy_lado.png").convert_alpha()
pacboy_baixo = pygame.image.load("sprites/pacboy_baixo.png").convert_alpha()
pacboy_cima = pygame.image.load("sprites/pacboy_cima.png").convert_alpha()

#Imagens da Direita
pacboy_direita1 = pacboy_lado.subsurface((0, 0), (20, 20))
pacboy_direita2 = pacboy_lado.subsurface((26, 1), (20, 20))
pacboy_direita3 = pacboy_lado.subsurface((47, 1), (20, 20))
pacboy_direita4 = pacboy_lado.subsurface((71, 2), (20, 20))

#Imagens da Esquerda
pacboy_esquerda1 = pygame.transform.flip(pacboy_direita1, 1, 0)
pacboy_esquerda2 = pygame.transform.flip(pacboy_direita2, 1, 0)
pacboy_esquerda3 = pygame.transform.flip(pacboy_direita3, 1, 0)
pacboy_esquerda4 = pygame.transform.flip(pacboy_direita4, 1, 0)

#Imagens de Baixo
pacboy_baixo1 = pacboy_baixo.subsurface((0, 1), (20, 20))
pacboy_baixo2 = pacboy_baixo.subsurface((24, 1), (20, 20))
pacboy_baixo3 = pacboy_baixo.subsurface((46, 0), (20, 20))
pacboy_baixo4 = pacboy_baixo.subsurface((70, 1), (20, 20))

#Imagens de Cima
pacboy_cima1= pacboy_cima.subsurface((0, 1), (20, 20))
pacboy_cima2 = pacboy_cima.subsurface((25, 1), (20, 20))
pacboy_cima3 = pacboy_cima.subsurface((49, 1), (20, 20))
pacboy_cima4 = pacboy_cima.subsurface((73, 1), (20, 20))

#imagem do Guug
inimigo_guug = pygame.image.load("sprites/guug.png").convert()
inimigo_guug.set_colorkey((255,255,255))

#imagem direita
inimigo1_esquerda1 = inimigo_guug.subsurface((55, 0), (20, 20))
inimigo1_esquerda2 = inimigo_guug.subsurface((70, 0), (20, 20))
inimigo1_esquerda3 = inimigo_guug.subsurface((86, 0), (20, 20))
#imagem esquerda
inimigo1_direita1 = pygame.transform.flip(inimigo1_esquerda1, 1, 0)
inimigo1_direita2 = pygame.transform.flip(inimigo1_esquerda2, 1, 0)
inimigo1_direita3 = pygame.transform.flip(inimigo1_esquerda3, 1, 0)
#imagem de cima
inimigo1_cima1 =  inimigo_guug.subsurface((104, 0), (20, 20))
inimigo1_cima2 =  inimigo_guug.subsurface((122, 0), (20, 20))
inimigo1_cima3 =  inimigo_guug.subsurface((140, 0), (20, 20))
#imagem de baixo
inimigo1_baixo1 = inimigo_guug.subsurface((1, 0), (20, 20))
inimigo1_baixo2 = inimigo_guug.subsurface((19, 0), (20, 20))
inimigo1_baixo3 = inimigo_guug.subsurface((37, 0), (20, 20))

#cenario
parede = pygame.image.load("sprites/parede.png").convert()
parede.set_colorkey((0, 0, 0))
parede2 = pygame.image.load("sprites/parede2.jpg").convert()
parede3 = pygame.image.load("sprites/parede3.png").convert()
parede4 = pygame.image.load("sprites/parede4.png").convert()
parede5 = pygame.image.load("sprites/parede5.jpg").convert()
parede6 = pygame.image.load("sprites/parede6.jpg").convert()
parede7 = pygame.image.load("sprites/parede7.png").convert()
parede8 = pygame.image.load("sprites/parede8.png").convert()
parede9 = pygame.image.load("sprites/parede9.jpg").convert()
parede10 = pygame.image.load("sprites/parede10.jpg").convert()
parede = {1: parede, 2: parede2}


#Pontuacao
vidas_pacboy = pygame.image.load("sprites/vidas_pacboy.png").convert_alpha()
texto_vidas = pygame.image.load("sprites/texto_vidas.png").convert_alpha()
texto_score = pygame.image.load("sprites/texto_score.png").convert_alpha()
texto_fim_de_jogo = pygame.image.load("sprites/texto_fim_de_jogo.png").convert_alpha()
texto_voce_ganhou = pygame.image.load("sprites/texto_voce_ganhou.png").convert_alpha()
relogio = pygame.image.load("sprites/relogio.png").convert_alpha()
icone_escudo = pygame.image.load("sprites/escudo.png").convert_alpha()

######################################################
####		Definicoes de Classes
######################################################

#inicializar os grupos

jogo = pygame.sprite.Group()
jogador = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
paredes = pygame.sprite.Group()
pontos = pygame.sprite.Group()
baus = pygame.sprite.Group()
portais = pygame.sprite.Group()
portoes = pygame.sprite.Group()
escudos = pygame.sprite.Group()
cenario = paredes, pontos, baus, portais, escudos, portoes, inimigos
all = pygame.sprite.RenderUpdates()

#class AI:
#	direcoes = {
#	"direita": exec("self.rect.x += 20"),
#	"esquerda": exec("self.rect.x -= 20"),
#	"baixo": exec("self.rect.y += 20"),
#	"cima": exec("self.rect.y -= 20)}

class Jogo(pygame.sprite.Sprite):
	estado = "jogando"
	fase = 1
	vidas = 3
	score = 0
	recordes_do_jogo = open("arquivos/recordes.pck")
	nome_do_jogador = ""
	bateu_recorde = None
	key = pygame.key.get_pressed()
	moveu_cenario = False
	moveu_cenario_distancia = 0
	direcao_oposta = {"direita":"esquerda","esquerda":"direita","cima":"baixo","baixo":"cima"}
	caminho_do_cenario = []

	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pygame.image.load("sprites/fundo1.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 0, 0
		
	def criar_fase(self):
		self.image = pygame.image.load("sprites/fundo%d.png"%self.fase).convert()
		pygame.mixer.music.stop()
		pygame.mixer.music.load("sons/musica_fase%d.mp3"%self.fase)
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)
		global tempo_inicial
		tempo_inicial = time()
		self.caminho_do_cenario = []
		if self.fase != 1:
			for grupo in cenario:
				grupo.empty()
			jogador.empty()
			inimigos.empty()
			all.empty()
			global pacboy
			pacboy = Pacboy()
			global guug
			guug = Guug(4)
		posx, posy = 0, 0
		for linha_da_tela in fase[self.fase]["mapa"]:
			for espaco in linha_da_tela:
				if espaco == "P":
					Parede(posx, posy)
				if espaco == "O":
					Portal(posx, posy)
				if espaco == "X":
					Portao(posx, posy)
				if espaco == "C":
					Bau(posx, posy)
				if espaco == "S":
					Escudo(posx, posy)
				if espaco == "E":
					if (posx, posy) != fase[self.fase]["pacboy_pos"]:
						posy += 5
						posx += 5
						Ponto(posx, posy)
						posy -= 5
						posx -= 5
				posx += 20
			posx = 0
			posy += 20

		if fase[self.fase]["mov_inicial"]:
			direcao = fase[self.fase]["mov_inicial"][0]
			distancia = fase[self.fase]["mov_inicial"][1]
			self.mover_cenario(direcao, distancia, False)
	
	def conferir_estado(self):
		if self.estado in ["Fim de Jogo", "Voce ganhou!", "Recordes", "Mensagem Recorde", "Voltar ao menu"]:
			if self.estado == "Recordes": self.recordes()
			else: self.mensagem()

	def recordes(self):
		if self.bateu_recorde == None:
			try:
				recorde = desencriptar(pickle.load(self.recordes_do_jogo))
				if int(recorde) <= self.score:
					self.recordes_do_jogo = open("arquivos/recordes.pck", "w")
					self.bateu_recorde = True
					self.estado = "Mensagem Recorde"
				else:
					self.bateu_recorde = False
					self.estado = "Voltar ao menu"
			except:
				self.recordes_do_jogo = open("arquivos/recordes.pck", "w")
				self.bateu_recorde = True
				self.estado = "Mensagem Recorde"
				
		if self.estado == "Mensagem Recorde":
			return

		if self.bateu_recorde: 
			if not self.key[pygame.K_RETURN]:
				self.input_nome()
			else:
				pickle.dump(encriptar(str(self.score)), self.recordes_do_jogo)
				pickle.dump(encriptar(self.nome_do_jogador), self.recordes_do_jogo)
				self.recordes_do_jogo.close()
				self.estado = "Voltar ao menu"
			tela.blit(texto_recorde, centralizar(texto_recorde, 70))
			tela.blit(texto_seu_nome, centralizar(texto_seu_nome, 100))
			
	def input_nome(self):
		def pegar_letra():
			def letra(caracter): 
				self.nome_do_jogador = self.nome_do_jogador + caracter

			self.key = pygame.key.get_pressed()
			pygame.event.wait()
			#for letra in "abcdefghijklemnopqrstwxyz0123456789":
			if self.key[pygame.K_a]: letra("A")
			elif self.key[pygame.K_b]: letra("B")
			elif self.key[pygame.K_c]: letra("C")
			elif self.key[pygame.K_d]: letra("D")
			elif self.key[pygame.K_e]: letra("E")
			elif self.key[pygame.K_f]: letra("F")
			elif self.key[pygame.K_g]: letra("G")
			elif self.key[pygame.K_h]: letra("H")
			elif self.key[pygame.K_i]: letra("I")
			elif self.key[pygame.K_j]: letra("J")
			elif self.key[pygame.K_k]: letra("K")
			elif self.key[pygame.K_l]: letra("L")
			elif self.key[pygame.K_m]: letra("M")
			elif self.key[pygame.K_n]: letra("N")
			elif self.key[pygame.K_o]: letra("O")
			elif self.key[pygame.K_p]: letra("P")
			elif self.key[pygame.K_q]: letra("Q")
			elif self.key[pygame.K_r]: letra("R")
			elif self.key[pygame.K_s]: letra("S")
			elif self.key[pygame.K_t]: letra("T")
			elif self.key[pygame.K_w]: letra("W")
			elif self.key[pygame.K_u]: letra("U")
			elif self.key[pygame.K_v]: letra("V")
			elif self.key[pygame.K_x]: letra("X")
			elif self.key[pygame.K_y]: letra("Y")
			elif self.key[pygame.K_z]: letra("Z")
			elif self.key[pygame.K_0]: letra("0")
			elif self.key[pygame.K_1]: letra("1")
			elif self.key[pygame.K_2]: letra("2")
			elif self.key[pygame.K_3]: letra("3")
			elif self.key[pygame.K_4]: letra("4")
			elif self.key[pygame.K_5]: letra("5")
			elif self.key[pygame.K_6]: letra("6")
			elif self.key[pygame.K_7]: letra("7")
			elif self.key[pygame.K_8]: letra("8")
			elif self.key[pygame.K_9]: letra("9")
			return self.nome_do_jogador
		
		if len(self.nome_do_jogador) <= 10: 
			nome = texto.render(pegar_letra(), True, (255, 255, 255))
		else: 
			nome = texto.render(self.nome_do_jogador, True, (255, 255, 255))
		tela.blit(nome, centralizar(nome, 200))

			
	def mensagem(self):
		if self.estado == "Voce ganhou!":
			tela.blit(texto_voce_ganhou, centralizar(texto_voce_ganhou))
			self.fase += 1
			if self.fase > 2: 
				self.estado = "Voltar ao menu"
			else: 
				self.estado = "jogando"
				pygame.display.update()
				pygame.time.wait(3000)
				self.criar_fase()
				return
		elif self.estado == "Fim de Jogo":
			pygame.mixer.music.set_volume(1)
			tela.blit(texto_fim_de_jogo, centralizar(texto_fim_de_jogo))
			self.estado = "Recordes"
		elif self.estado == "Mensagem Recorde":
			tela.blit(texto_recorde, centralizar(texto_recorde, 70))
			tela.blit(texto_seu_nome, centralizar(texto_seu_nome, 100))
			self.estado = "Recordes"
		pygame.display.update()
		pygame.time.wait(3000)


	
	def reset_cenario_pos(self, caminho_do_cenario):
		for caminho in caminho_do_cenario:
			self.mover_cenario(self.direcao_oposta[caminho[0]], caminho[1], False)

	def mover_cenario(self, direcao, distancia, add_caminho = True):
		for grupo in cenario:
			for sprite in grupo:
				if direcao == "direita": sprite.rect[0] -= distancia
				elif direcao == "esquerda": sprite.rect[0] += distancia
				elif direcao == "baixo": sprite.rect[1] -= distancia
				elif direcao == "cima": sprite.rect[1] += distancia

		if add_caminho:
			self.moveu_cenario = direcao
			self.moveu_cenario_distancia = distancia
			self.caminho_do_cenario.append([direcao, distancia])
	
	def reiniciar_fase(self):
		pygame.mixer.music.stop()
		self.reset_cenario_pos(jogo_corrente.caminho_do_cenario)
		self.caminho_do_cenario = []
		pygame.time.wait(2000)
		pygame.mixer.music.play(-1)

	def teletransportar(self, player, distancia):
		som_teletransportar.play(0)
		if player.rect.x > LARGURA_DA_TELA/2: 
			player.rect.x -= fase[self.fase]["largura_da_fase"] - distancia
			self.mover_cenario("esquerda", distancia)
		else: 
			player.rect.x += fase[self.fase]["largura_da_fase"] - distancia
			self.mover_cenario("direita", distancia)
	
class Colisao:
	def colisao(self, objeto, grupo, grupo2 = None, exclusao = False):
		"""Verifica se ha colisoes entre um objeto e um outro grupo de objetos. """
		if grupo2 != None:
			if len(pygame.sprite.spritecollide(objeto, grupo, exclusao)) == 0 and \
			len(pygame.sprite.spritecollide(objeto, grupo2, exclusao)) == 0: return False
			else: return True
		if len(pygame.sprite.spritecollide(objeto, grupo, exclusao)) == 0: return False
		else: return True

class Parede(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = parede[jogo_corrente.fase]
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		paredes.add(self)

class Ponto(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pygame.image.load("sprites/super_bola.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		pontos.add(self)

class Portal(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pygame.image.load("sprites/portal.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		portais.add(self)

class Portao(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pygame.image.load("sprites/portao.png").convert_alpha()
		self.image.set_colorkey((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		portoes.add(self)

class Bau(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pygame.image.load("sprites/bau.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		baus.add(self)


class Escudo(pygame.sprite.Sprite):
	def __init__(self, posx, posy):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = icone_escudo
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posx, posy
		escudos.add(self)


class Pacboy(pygame.sprite.Sprite, Colisao):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = pacboy_direita2
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = fase[jogo_corrente.fase]["pacboy_pos"]
		self.velocidade = 2
		self.tempo_de_animacao = 0
		self.direcao = None
		self.ultima_direcao = None
		self.direcao_oposta = {"direita":"esquerda","esquerda":"direita","cima":"baixo","baixo":"cima"}
		self.defende = 0
		self.tempo_com_escudo = 0
		self.atualizar = True
		self.colide = False
		
	def move(self, direcao):
		#if (self.direcao != direcao) and (jogo_corrente.moveu_cenario):
		#	self.direcao = direcao
		print("Posição do personagem: x: %d y: %d" %( self.rect.x/(len(fase[1]["mapa"][0])), self.rect.y/(len(fase[1]["mapa"]))))

		
		if (self.rect.x % 20 == 0 and self.rect.y % 20 == 0): 
			self.direcao = direcao
		else:
			if self.direcao != direcao:
				self.ultima_direcao = direcao
				self.atualizar = False
			else:
				self.atualizar = True

	def andar(self, direcao):
		if self.colisao(self, portais): 
			jogo_corrente.teletransportar(self, fase[jogo_corrente.fase]["portal"])
			return

		if direcao == "direita":
			if self.rect.x > (LARGURA_DA_TELA - 80):
				jogo_corrente.mover_cenario(direcao, self.velocidade)
			else:
				jogo_corrente.moveu_cenario = False
				self.rect.x += self.velocidade
			if self.colisao(self, paredes, portoes): 
				self.colide = True
				self.rect.x -= self.velocidade
			else: self.colide = False
		elif direcao == "esquerda": 
			if self.rect.x < 80: 
				jogo_corrente.mover_cenario(direcao, self.velocidade)
			else:
				jogo_corrente.moveu_cenario = False
				self.rect.x -= self.velocidade
			if self.colisao(self, paredes, portoes): 
				self.colide = True
				self.rect.x += self.velocidade
			else: self.colide = False
		elif direcao == "baixo": 
			if self.rect.y > ALTURA_DA_TELA - 80: 
				jogo_corrente.mover_cenario(direcao, self.velocidade)
			else:
				jogo_corrente.moveu_cenario = False
				self.rect.y += self.velocidade
			if self.colisao(self, paredes, portoes): 
				self.colide = True
				self.rect.y -= self.velocidade
			else: self.colide = False
		elif direcao == "cima":
			if self.rect.y < 80: 
				jogo_corrente.mover_cenario(direcao, self.velocidade)
			else:
				jogo_corrente.moveu_cenario = False
				self.rect.y -= self.velocidade
			if self.colisao(self, paredes, portoes): 
				self.colide = True
				self.rect.y += self.velocidade
			else: self.colide = False

	def animacao(self, direcao):
		"""Faz a dinamica entre as sprites contralada pelo tempo de animacao(frames)."""
		self.tempo_de_animacao += 1
		if direcao == "direita":
			if self.tempo_de_animacao <= 5: self.image = pacboy_direita1
			elif 5 < self.tempo_de_animacao <= 10: self.image = pacboy_direita2
			elif 10 < self.tempo_de_animacao <= 15: self.image = pacboy_direita3
			elif 15 < self.tempo_de_animacao <= 20: self.image = pacboy_direita4
		elif direcao == "esquerda":
			if self.tempo_de_animacao <= 5: self.image = pacboy_esquerda1
			elif 5 < self.tempo_de_animacao <= 10: self.image = pacboy_esquerda2
			elif 10 < self.tempo_de_animacao <= 15: self.image = pacboy_esquerda3
			elif 15 < self.tempo_de_animacao <= 20: self.image = pacboy_esquerda4
		elif direcao == "baixo":
			if self.tempo_de_animacao <= 5: self.image = pacboy_baixo1
			elif 5 < self.tempo_de_animacao <= 10: self.image = pacboy_baixo2
			elif 10 < self.tempo_de_animacao <= 15: self.image = pacboy_baixo3
			elif 15 < self.tempo_de_animacao <= 20: self.image = pacboy_baixo4
		elif direcao == "cima":
			if self.tempo_de_animacao <= 5: self.image = pacboy_cima1
			elif 5 < self.tempo_de_animacao <= 10: self.image = pacboy_cima2
			elif 10 < self.tempo_de_animacao <= 15: self.image = pacboy_cima3
			elif 15 < self.tempo_de_animacao <= 20: self.image = pacboy_cima4

		if self.tempo_de_animacao == 20: self.tempo_de_animacao = 0

	def update(self):
		"""Atualiza qualquer alteracao de movimento ou animacao."""
		self.andar(self.direcao)
		if not self.colide:
			self.animacao(self.direcao)

class Guug(pygame.sprite.Sprite, Colisao):
	def __init__(self, inimigo_numero):
		pygame.sprite.Sprite.__init__(self, self.container)
		self.image = inimigo1_baixo1
		self.rect = self.image.get_rect()
		posicao_inicial = fase[jogo_corrente.fase]["inimigo_pos"]
		self.rect.x, self.rect.y = posicao_inicial
		self.inimigo = inimigo_numero
		self.direcao_oposta = {"direita":"esquerda","esquerda":"direita","cima":"baixo","baixo":"cima"}
		self.velocidade = 1
		self.tempo_de_animacao = 0
		self.direcao = None
		self.ultima_direcao = None
		self.atualizar = True
		self.movimento = 0
		movimento_inicial = fase[jogo_corrente.fase]["mov_inicial"]
		if len(jogo_corrente.caminho_do_cenario) > 0:
			for move in jogo_corrente.caminho_do_cenario:
				self.andar(self.direcao_oposta[move[0]], move[1])
		else:
			if movimento_inicial:
				self.andar(movimento_inicial[0], movimento_inicial[1])

		
	def move(self):
		if self.inimigo == 4:
			if self.direcao == None:
				if self.rect.y < pacboy.rect.y: self.direcao = "baixo"
				elif self.rect.y > pacboy.rect.y: self.direcao = "cima"
				elif self.rect.x < pacboy.rect.x: self.direcao = "direita"
				elif self.rect.x > pacboy.rect.x: self.direcao = "esquerda"
			else:
				self.direcao = None

	def andar(self, direcao, velocidade):
		if direcao == "direita": 
			self.rect.x += velocidade
		elif direcao == "esquerda":
			self.rect.x -= velocidade
		elif direcao == "baixo": 
			self.rect.y += velocidade
		elif direcao == "cima": 
			self.rect.y -= velocidade

	def animacao(self, direcao):
		"""Faz a dinamica entre as sprites contralada pelo tempo de animacao (frames)."""
		self.tempo_de_animacao += 1
		if direcao == "direita":
			if self.tempo_de_animacao <= 5: self.image = inimigo1_direita1
			elif 5 < self.tempo_de_animacao <= 10: self.image = inimigo1_direita2
			elif 10 < self.tempo_de_animacao <= 15: self.image = inimigo1_direita3

		elif direcao == "esquerda":
			if self.tempo_de_animacao <= 5: self.image = inimigo1_esquerda1
			elif 5 < self.tempo_de_animacao <= 10: self.image = inimigo1_esquerda2
			elif 10 < self.tempo_de_animacao <= 15: self.image = inimigo1_esquerda3

		elif direcao == "baixo":
			if self.tempo_de_animacao <= 5: self.image = inimigo1_baixo1
			elif 5 < self.tempo_de_animacao <= 10: self.image = inimigo1_baixo2
			elif 10 < self.tempo_de_animacao <= 15: self.image = inimigo1_baixo3

		elif direcao == "cima":
			if self.tempo_de_animacao <= 5: self.image = inimigo1_cima1
			elif 5 < self.tempo_de_animacao <= 10: self.image = inimigo1_cima2
			elif 10 < self.tempo_de_animacao <= 15: self.image = inimigo1_cima3

		if self.tempo_de_animacao == 15: self.tempo_de_animacao = 0

	def update(self):
		"""Atualiza as alteracoes do objeto."""
		if self.colisao(self, portoes):
			abrir_portao.play()
		self.move()
		self.animacao(self.direcao)
		self.movimento += 1
		if self.movimento > 2:
			self.andar(self.direcao, self.velocidade)
			self.movimento = 0

class Buxh(pygame.sprite.Sprite, Colisao):
	pass

Jogo.container = jogo
Pacboy.container = jogador, all
Guug.container = inimigos, all
Parede.container = paredes, all
Ponto.container = pontos, all
Bau.container = baus, all
Portal.container = portais, all
Portao.container = portoes, all
Escudo.container = escudos, all

##################################################
####		Definicoes de funcoes
##################################################

def numeros_em_sprite(numero):
	sprite = []
	for digito in str(numero):
		if digito == "0":
			sprite.append(pygame.image.load("sprites/0.gif").convert_alpha())
		elif digito == "1":
			sprite.append(pygame.image.load("sprites/1.gif").convert_alpha())
		elif digito == "2":
			sprite.append(pygame.image.load("sprites/2.gif").convert_alpha())
		elif digito == "3":
			sprite.append(pygame.image.load("sprites/3.gif").convert_alpha())
		elif digito == "4":
			sprite.append(pygame.image.load("sprites/4.gif").convert_alpha())
		elif digito == "5":
			sprite.append(pygame.image.load("sprites/5.gif").convert_alpha())
		elif digito == "6":
			sprite.append(pygame.image.load("sprites/6.gif").convert_alpha())
		elif digito == "7":
			sprite.append(pygame.image.load("sprites/7.gif").convert_alpha())
		elif digito == "8":
			sprite.append(pygame.image.load("sprites/8.gif").convert_alpha())
		elif digito == "9":
			sprite.append(pygame.image.load("sprites/9.gif").convert_alpha())
	return sprite

def centralizar(imagem, pos_y = False, mod_x = 0):
	imagem_rect = imagem.get_rect()
	if pos_y: imagem_posy = pos_y
	else: imagem_posy = ALTURA_DA_TELA/2 - imagem_rect[3]/2
	if mod_x: 
		imagem_posx = (LARGURA_DA_TELA/2 - imagem_rect[2]/2) - mod_x
		return (imagem_posx, imagem_posy)
	else: imagem_posx = LARGURA_DA_TELA/2 - imagem_rect[2]/2

	return (imagem_posx, imagem_posy)

def conferir_entradas(TELA_CHEIA):
	if pygame.key.get_pressed()[pygame.K_RIGHT]: 
		pacboy.move("direita")
	elif pygame.key.get_pressed()[pygame.K_LEFT]: 
		pacboy.move("esquerda")
	elif pygame.key.get_pressed()[pygame.K_DOWN]: 
		pacboy.move("baixo")
	elif pygame.key.get_pressed()[pygame.K_UP]: 
		pacboy.move("cima")

def pontuacao():
	for ponto in pygame.sprite.spritecollide(pacboy, pontos, True):
		jogo_corrente.score += 1
	for ponto in pygame.sprite.spritecollide(pacboy, baus, True):
		capturou_bau.play()
		jogo_corrente.score += 10
	for escudo in pygame.sprite.spritecollide(pacboy, escudos, True):
		pacboy.defende += 1
		pacboy.tempo_com_escudo = time() - tempo_inicial
		pegou_escudo.play()
		pygame.mixer.music.set_volume(1)

	if (time() - tempo_inicial) - pacboy.tempo_com_escudo > 10:
		pacboy.defende = False
		pygame.mixer.music.set_volume(0.5)

	#Blita as vidas do Pacboy
	tela.blit(texto_vidas, (0, 0))
	for vida in xrange(jogo_corrente.vidas):
		tela.blit(vidas_pacboy, (50 + (20 * vida), 0))
	#Blita o Score
	tela.blit(texto_score, (300, 0))
	score = numeros_em_sprite(jogo_corrente.score)
	for digito, digito_pos in zip(score, xrange(len(score))):
		tela.blit(digito, (350 + (digito_pos * 10), 5))
	#Blita o tempo
	tela.blit(relogio, ((LARGURA_DA_TELA/2 - 30), 0))
	tempo_atual = time() - tempo_inicial
	tempo = numeros_em_sprite(int(tempo_atual))
	for digito, digito_pos in zip(tempo, xrange(2)):
		tela.blit(digito, ((LARGURA_DA_TELA/2 - 10) + (digito_pos * 10), 5))
	#Blita o escudo ( caso tenha )
	if pacboy.defende:
		pacboy.tempo_com_escudo = time() - pacboy.tempo_com_escudo
		tela.blit(icone_escudo, ((275), 0))

def criaListaDeArestas(mapa):
	tamanhoY = len(mapa)
	tamanhoX = len(mapa[0])

	#print "Iniciando a transformacao de uma matriz " + str(tamanhoX) + " por " + str(tamanhoY) + " em uma lista de arestas\n"
	
	#print "Normalizando baus,escudos e portais em espacos\n"
	
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

################################################
####		Inicializar o Jogo
################################################

#Criar fase

fase = {
1: {
"pacboy_pos": (180, 180),
"mov_inicial": False,
"inimigo_pos": (180, -30),
"portal": 100,
"largura_da_fase": 340,
"mapa": [
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
"PPPPPPPPPPPPPPPPPPPP"]},
2: {
"pacboy_pos": (180, 200),
"mov_inicial": ["direita", 60],
"inimigo_pos": (180, -30),
"portal": 300,
"largura_da_fase": 460,
"mapa": [
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
"PPPPPPPPPPPPPPPPPPPPPPPPPP"]}}


#Tempo
tempo_inicial=  time() 	#em segundos

#Objetos
jogo_corrente = Jogo()
pacboy = Pacboy()
guug = Guug(4)

jogo_corrente.criar_fase()

#Loop principal
TELA_CHEIA = False
jogando = True
fps = []
criaListaDeArestas(fase[1]["mapa"])

while jogando:
	jogo_corrente.key = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT or jogo_corrente.key[pygame.K_ESCAPE]:
			jogando = False

	if jogo_corrente.key[pygame.K_f]:
		TELA_CHEIA = not TELA_CHEIA
		if TELA_CHEIA: 
			tela = pygame.display.set_mode(TAMANHO_DA_TELA, 0, 32)
		else: 
			tela = pygame.display.set_mode(TAMANHO_DA_TELA, FULLSCREEN, 32)
	if jogo_corrente.estado == "Voltar ao menu":
		jogando = False

	all.clear(tela, tela)
	all.update()

	if jogo_corrente.estado == "jogando":
		fps.append(tempo.get_fps())
		conferir_entradas(TELA_CHEIA)

		if pacboy.defende: pacboy_escudo = False
		else: pacboy_escudo = True
		
		for player in pygame.sprite.groupcollide(jogador, inimigos, pacboy_escudo, True):
			if pacboy.defende:
				inimigo_morreu.play()
				jogo_corrente.score += 20
				guug = Guug(4)
			else:
				grito_de_morte.play()
				jogo_corrente.vidas -= 1
				if jogo_corrente.vidas < 1:
					jogo_corrente.estado = "Fim de Jogo"
				else:
					pacboy = Pacboy()
					guug = Guug(4)
					jogo_corrente.reiniciar_fase()

		if (time() - tempo_inicial) > 99:
			jogo_corrente.estado = "Fim de Jogo"

		if len(pontos) == 0:
			jogo_corrente.estado = "Voce ganhou!"
			pygame.mixer.music.stop()
			som_ganhou.play()

			
	jogo.draw(tela)
	all.draw(tela)
	
	pontuacao()
	jogo_corrente.conferir_estado()
		
	pygame.display.update()
	tempo.tick(60)


print ("Media de FPS no ultimo jogo: %.1f"%(sum(fps) / len(fps)))

