# -*- coding:utf-8 -*-

from distutils.log import error
import copy

class IlluminatiEngine:

	def __init__(self):
		self.linhas = 0
		self.colunas = 0
		self.historico = []

	def ler_tabuleiro_ficheiro(self, filename):
		'''
		comando cria nova instancia do jogo
		parâmetro: nome do ficheiro
		'''
		try:
			ficheiro = open(filename, "r")
			lines = ficheiro.readlines()
			# obter os dois numeros da dimensao do puzzle, retirando o '\n'
			dim = lines[0].strip('\n').split(' ')
			self.linhas = int(dim[0])  # retirar o numero de linhas
			self.colunas = int(dim[1])  # retirar o numero de colunas
			# remover primeira linha da lista de linhas pois ja nao precisamos
			del lines[0]
			self.historico = []
			tabuleiro = []
			for line in lines:
				tabuleiro.append(line.split())
			self.settabuleiro(tabuleiro)
			estado = True
		except:
			print("Erro: na leitura do tabuleiro")
			estado = False
		else:
			ficheiro.close()
		return estado

	def gravar_tabuleiro_ficheiro(self, filename):
		'''comando grava a instancia do jogo
		parâmetro: nome do ficheiro
		'''
		try:
			ficheiro = open(filename, "w+")  # abre o ficheiro para escrita
			# escrever na 1º linha do ficheiro
			ficheiro.write(str(self.colunas) + ' ' + str(self.linhas) + '\n')
			# último tabuleiro alterado
			ultimo_tabuleiro = self.historico.index(len(self.historico) - 1)
			for linha in ultimo_tabuleiro:
				linha_f = ''
				for coluna in linha:
					linha_f = linha_f + coluna + ' '
				ficheiro.write(linha_f + '\n')
			estado = True
		except:
			print("Erro: ao guardar o tabuleiro no ficheiro:" + filename)
			estado = False
		else:
			ficheiro.close()
		return estado

	def gravar_historico(self, filename):
		'''comando grava todas as instancias do jogo
		parâmetro: nome do ficheiro
		'''
		try:
			ficheiro = open(filename, "w+")  # abre o ficheiro para escrita
			# escrever na 1º linha do ficheiro
			ficheiro.write(str(self.colunas) + ' ' + str(self.linhas) + '\n')
			for tabuleiro in self.historico:
				for linha in tabuleiro:
					linha_f = ''
					for coluna in linha:
						linha_f = linha_f + coluna + ' '
					ficheiro.write(linha_f + '\n')
				ficheiro.write('\n')
		except:
			print("Erro: ao guardar o tabuleiro no ficheiro:" + filename)
		else:
			ficheiro.close()

	def getlinhas(self):
		'''comando devolve as linhas do tabuleiro
		'''
		return self.linhas

	def getcolunas(self):
		'''comando devolve as colunas do tabuleiro
		'''
		return self.colunas

	def gettabuleiro(self):
		'''comando devolve uma cópia do último tabuleiro
		'''
		# devolver uma cópia do original para não alterar o tabuleiro no histórico
		return copy.deepcopy(self.historico[len(self.historico) - 1])

	def settabuleiro(self, t):
		'''comando faz uma cópia do ficheiro original
		'''
		# recebemos um tabuleiro e criamos uma cópia para nos tornarmos imunes a alterações ao tabuleiro original
		c = copy.deepcopy(t)
		self.historico.append(c)

	# implementar os metodos que permitem resolver/jogar o puzzle
	def verifica_tabuleiro(self):
		'''comando verifica se o tabuleiro foi carregado ou não
		'''
		# Se não houver tabuleiro
		if self.gettabuleiro() == []:
			print("Tabuleiro não carregado!")
			# devolve falso, não existe tabuleiro carregado
			return False
		return True

	def so_iluminado_por_ele(self, tabuleiro, i, j):
		'''comando que permite ver se uma posição está rodeada por casas onde não pode
		haver lâmpadas
		parâmetros: tabuleiro, linha, coluna
		'''
		# variável com todas as casas bloqueantes
		bloqueante = ["x", "0", "1", "2", "3", "4"]
		if tabuleiro[i][j] in bloqueante:
			return False
		# Enquanto i >= 0 e não houver uma casa bloqueante acima
		cursor = i - 1
		while cursor >= 0 and tabuleiro[cursor][j] not in bloqueante:
			# Se existir um "-" ou uma lampada nesta posição
			if tabuleiro[cursor][j] == '-' or tabuleiro[cursor][j] == '@':
				# Return False
				return False
			cursor -= 1
		# Enquanto i < len(tabuleiro) e não houver uma casa bloqueante abaixo
		cursor = i + 1
		while cursor < len(tabuleiro) and tabuleiro[cursor][j] not in bloqueante:
			# Se existir um "-" nesta posição
			if tabuleiro[cursor][j] == '-' or tabuleiro[cursor][j] == '@':
				return False
			cursor += 1
		# Enquanto j >= 0 e não houver uma casa bloqueante à esquerda
		cursor = j - 1
		while cursor >= 0 and tabuleiro[i][cursor] not in bloqueante:
			# Se exisitr um "-" nesta posição
			if tabuleiro[i][cursor] == '-' or tabuleiro[i][cursor] == '@':
				return False
			cursor -= 1
		# Enquanto j < len(line) e não houver uma casa bloqueante à direita
		cursor = j + 1
		while cursor < len(tabuleiro[i]) and tabuleiro[i][cursor] not in bloqueante:
			# Se existir um "-" nesta posição
			if tabuleiro[i][cursor] == '-' or tabuleiro[i][cursor] == '@':
				return False
			cursor += 1
		# Caso contrário, esta posição só pode ser iluminada por uma lampada nessa posição
		return True

	def undo(self):
		'''comando que permite desfazer as ações de um passo anterior
		'''
		# Se houver histórico
		if len(self.historico) > 1:
			# removemos o último estado
			self.historico.pop()
		# Devolver o último tabuleiro
		return self.gettabuleiro()

	def tabuleiro_identico(self, a, b):
		'''comando verifica se os dois tabuleiros são ou não iguais
		parâmetro: tabuleiro a, tabuleiro b
		'''
		# Se os tabuleiros forem diferentes
		if len(a) != len(b):
			return False
		for i, line in enumerate(a):
			# Se as linhas forem diferentes
			if len(a[i]) != len(b[i]):
				return False
			for j, caracter in enumerate(line):
				# Se as posições forem diferentes
				if a[i][j] != b[i][j]:
					return False
		# Caso contrário
		return True

	def proxima_casa_disponivel(self, tabuleiro):
		'''comando que permite obter a primeira posição do tabuleiro que está vazia
		parâmetro: tabuleiro
		'''
		for i, line in enumerate(tabuleiro):
			for j, caracter in enumerate(line):
				# Se na posição temos um '-'
				if tabuleiro[i][j] == "-":
					# devolver as coordenadas dessa posição
					return (i, j)
		# Caso contrário
		return None
