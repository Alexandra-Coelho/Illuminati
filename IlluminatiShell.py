# -*- coding:utf-8 -*-

from cmd import Cmd
import copy
from re import T
from IPython.display import clear_output
from IlluminatiWindow import IlluminatiWindow
from IlluminatiEngine import IlluminatiEngine


class IlluminatiShell(Cmd):
	'''Classe que implementa todas as funções que permitem realizar jogadas e guardar o estado do puzzle \n'''
	intro = 'Illuminati shell.   Type help or ? to list commands.\n'
	prompt = 'Illuminati> '

	def print_puzzle(self, puzzle):
		'''comando que permite imprimir o tabuleiro na consola
		parâmetro: tabuleiro
		'''
		clear_output(wait=True)
		i = 1
		print(" ", end=" ")
		for col_num in range(1, len(puzzle[0])+1):
			print(f"{col_num:2d}", end="")
		print()
		for linha in puzzle:
			print(f"{i:2d}", end=" ")
			i += 1
			for simbolo in linha:
				print(simbolo, end=" ")
			print()

	def do_mr(self, arg):
		'''comando que permite mostrar o tabuleiro existente num ficheiro
		parâmetro: nome do ficheiro
		'''
		lista_arg = arg.split()
		try:
			lista_arg = arg.split()
			eng.ler_tabuleiro_ficheiro(lista_arg[0])
			self.print_puzzle(eng.gettabuleiro())
			global janela  # pois pretendo atribuir um valor a um identificador global
			if janela is not None:
				del janela  # invoca o metodo destruidor de instancia __del__()
			janela = IlluminatiWindow(40, eng.getlinhas(), eng.getcolunas())
			janela.mostraJanela(eng.gettabuleiro())
		except Exception as e:
			print("Erro: ", e)

	def do_cr(self, arg):
		'''comando que permite carregar um tabuleiro de um ficheiro na memória
		parâmetro: nome do ficheiro
		'''
		lista_arg = arg.split()
		try:
			lista_arg = arg.split()
			eng.ler_tabuleiro_ficheiro(lista_arg[0])
			self.print_puzzle(eng.gettabuleiro())
			global janela  # pois pretendo atribuir um valor a um identificador global
			if janela is not None:
				del janela  # invoca o metodo destruidor de instancia _del_()
			janela = IlluminatiWindow(40, eng.getlinhas(), eng.getcolunas())
			janela.mostraJanela(eng.gettabuleiro())
		except Exception as e:
			print("Erro: ", e)

	def do_gr(self, arg):
		'''comando que permite gravar o estado do tabuleiro atual
		parâmetro: nome de um ficheiro
		'''
		try:
			lista_arg = arg.split()
			eng.gravar_tabuleiro_ficheiro(lista_arg[0])
			print("Tabuleiro guardado no ficheiro:" + lista_arg[0])
		except Exception as e:
			print("Erro: ", e)

	def do_grh(self, filename):
		'''comando que permite gravar todas as alterações passo a passo do tabuleiro
		parâmetro: nome de um ficheiro
		'''
		eng.gravar_historico(filename)

	def do_jg(self, tabuleiro, coluna, linha):
		'''comando que permite realizar jogadas manualmente no tabuleiro
		parâmetro: tabuleiro, dois inteiros com o número da coluna e linha
		'''
		caracter = tabuleiro[linha-1][coluna-1]
		# se nesta casa tiver um '-'
		if caracter == "-":
			# coloca uma lâmpada
			tabuleiro[linha-1][coluna-1] = "@"
		# se nesta casa tiver uma lâmpada
		elif caracter == "@":
			# retirar lâmpada
			tabuleiro[linha-1][coluna-1] = "-"
		# noutra condição
		else:
			print("Casa bloqueada")
		return tabuleiro

	def do_mi(self, tabuleiro):
		'''comando que permite iluminar o tabuleiro quando encontra um '.'
		parâmetro: tabuleiro
		'''
		novo_tabuleiro = self.do_est2(tabuleiro)
		for i, line in enumerate(novo_tabuleiro):
			for j, caracter in enumerate(line):
				if caracter == ".":
					novo_tabuleiro[i][j] = "o"
		return novo_tabuleiro

	def do_est1(self, tabuleiro):
		'''comando que permite realizar a estratégia 1 onde colocada lâmpadas
		se o nº de casas vizinhas for igual ao número da casa bloqueada
		parâmetro: tabuleiro
		'''
		tab = copy.deepcopy(tabuleiro)
		# Ciclo para percorrer as linhas do tabuleiro -> retorna cada linha
		for i, line in enumerate(tab):
			# Ciclo para percorrer as colunas da linha retornada -> retorna caracter
			for j, caracter in enumerate(line):
				# Se tivermos um valor entre 1 e 4
				if caracter in ["1", "2", "3", "4"]:
					# Inicializar quantidade de traços a zero
					num_tracos = 0
					# Contar quantidade de traços à volta deste número
					# Verificar se existe um traço acima
					if i > 0:
						if tab[i-1][j] == "-" or tab[i-1][j] == "@":
							num_tracos += 1
					# Verificar se existe um traço abaixo
					if i < len(tab)-1:
						if tab[i+1][j] == "-" or tab[i+1][j] == "@":
							num_tracos += 1
					# Verificar se existe um traço à esquerda
					if j > 0:
						if tab[i][j-1] == "-" or tab[i][j-1] == "@":
							num_tracos += 1
					# Verificar se existe um traço à direita
					if j < len(line) - 1:
						if tab[i][j+1] == "-" or tab[i][j+1] == "@":
							num_tracos += 1
					# Se o número da casa for igual à quantidade de traços à volta
					if int(caracter) == num_tracos:
						# Colocar lampadas nessas posições
						# Verificar se existe um traço acima
						if i > 0:
							if tab[i-1][j] == "-":
								tab[i-1][j] = '@'
						# Verificar se existe um traço abaixo
						if i < len(tab)-1:
							if tab[i+1][j] == "-":
								tab[i+1][j] = '@'
						# Verificar se existe um traço à esquerda
						if j > 0:
							if tab[i][j-1] == "-":
								tab[i][j-1] = '@'
						# Verificar se existe um traço à direita
						if j < len(line) - 1:
							if tab[i][j+1] == "-":
								tab[i][j+1] = '@'
		return tab

	def do_est2(self, tabuleiro):
		'''comando que permite realizar a estratégia 2 que ilumina a coluna e a linha onde existe
		uma lâmpada até encontrarmos o limite do tabuleiro ou uma casa bloqueada
		parâmetro: tabuleiro
		'''
		tab = copy.deepcopy(tabuleiro)
		# Inicializar casas bloqueantes
		bloqueada = ['x', '0', '1', '2', '3', '4']
		# Ciclo para percorrer as linhas do tabuleiro -> retorna cada linha
		for i, line in enumerate(tab):
			# Ciclo para percorrer as colunas da linha retornada -> retorna caracter
			for j, caracter in enumerate(line):
				# Se houver uma lampada nesta casa
				if tab[i][j] == '@':
					# Enquanto não encontrarmos uma casa bloqueada ou o fim do mapa para a esquerda
					cursor = j-1
					while cursor >= 0 and tab[i][cursor] not in bloqueada:
						# Colocar pontos
						tab[i][cursor] = '.'
						# Decrementar cursor
						cursor -= 1
					# Enquanto não encontrarmos uma casa bloqueada ou o fim do mapa para a direita
					cursor = j + 1
					while cursor < len(line) and tab[i][cursor] not in bloqueada:
						# Colocar pontos
						tab[i][cursor] = '.'
						# Incrementar cursor
						cursor += 1
					# Enquanto não encontrarmos uma casa bloqueada ou o fim do mapa para cima
					cursor = i - 1
					while cursor >= 0 and tab[cursor][j] not in bloqueada:
						# Colocar pontos
						tab[cursor][j] = '.'
						# Decrementar cursor
						cursor -= 1
					# Enquanto não encontrarmos uma casa bloqueada ou o fim do mapa para baixo
					cursor = i + 1
					while cursor < len(tab) and tab[cursor][j] not in bloqueada:
						# Colocar pontos
						tab[cursor][j] = '.'
						# Incrementar cursor
						cursor += 1
		return tab

	def do_est3(self, tabuleiro):
		'''comando que permite realizar a estratégia 3 que coloca '.' em casas onde uma lâmpada
		causaria uma contradição
		parâmetro: tabuleiro
		'''
		tab = copy.deepcopy(tabuleiro)
		# Ciclo para percorrer as linhas do tabuleiro -> retorna cada linha
		for i, line in enumerate(tab):
			# Ciclo para percorrer as colunas da linha retornada -> retorna caracter
			for j, caracter in enumerate(line):
				# Se o caracter atual for "-"
				if caracter == '-':
					# Se eu não estiver na primeira linha e houver um 0 acima
					if i > 0 and tab[i - 1][j] == "0":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na última linha e houver um 0 abaixo
					if i < len(tab) - 1 and tab[i + 1][j] == "0":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na primeira coluna e houver um 0 à esquerda
					if j > 0 and tab[i][j - 1] == "0":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na última coluna e houver um 0 à direita
					if j < len(line) - 1 and tab[i][j + 1] == "0":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na primeira linha nem na primeira coluna e houver um 4 acima à esquerda
					if i > 0 and j > 0 and tab[i - 1][j - 1] == "4":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na primeira linha nem na última coluna ee houver um 4 acima à direita
					if i > 0 and j < len(line) - 1 and tab[i - 1][j + 1] == "4":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na última linha nem na última coluna e houver um 4 abaixo à direita
					if i < len(tab) - 1 and j < len(line) - 1 and tab[i + 1][j + 1] == "4":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
					# Se eu não estiver na última linha nem na primeira coluna e houver um 4 abaixo à esquerda
					if i < len(tab) - 1 and j > 0 and tab[i + 1][j - 1] == "4":
						# Esta posição passa a ser um "."
						tab[i][j] = '.'
		return tab

	def do_est4(self, tabuleiro):
		'''comando que permite realizar a estratégia 4 onde não podemos colocar lâmpadas nas duas casas
		partilhadas em diagonal por conjuntos específicos de números (0 e 2), (1 e 3) e colocamos lâmpadas
		obrigatoriamente nas 2 outras posições livres (para o 2 e o 3)
		parâmetro: tabuleiro
		'''
		tab = copy.deepcopy(tabuleiro)
		# Ciclo para percorrer as linhas do tabuleiro -> retorna cada linha
		for i, line in enumerate(tab):
			# Ciclo para percorrer as colunas da linha retornada -> retorna caracter
			for j, caracter in enumerate(line):
				# Se caracter for 0
				if caracter == "0":
					# Se não estivermos na primeira linha nem na primeira coluna e houver um 2 acima à esquerda
					if i > 0 and j > 0 and tab[i - 1][j - 1] == "2":
						# Colocar uma lampada acima do 2
						tab[i - 2][j - 1] = '@'
						# Colocar uma lampada à esquerda do 2
						tab[i - 1][j - 2] = '@'
					# Se não estivermos na primeira linha nem na última coluna e houver um 2 acima à direita
					if i > 0 and j < len(line) - 1 and tab[i - 1][j + 1] == "2":
						# Colocar uma lampada acima do 2
						tab[i - 2][j + 1] = '@'
						# Colocar uma lampada à direita do 2
						tab[i - 1][j + 2] = '@'
					# Se não estivermos na útlima linha, última coluna e houver um 2 abaixo à direita
					if i < len(tab) - 1 and j < len(line) -1 and tab[i + 1][j + 1] == "2":
						# Colocar uma lampada abaixo do 2
						tab[i + 2][j + 1] = '@'
						# Colocar uma lampada à direita do 2
						tab[i + 1][j + 2] = '@'
					# Se não estivermos na última linha, primeira coluna e houver um 2 abaixo à esquerda
					if i < len(tab) - 1 and j > 0 and tab[i + 1][j - 1] == "2":
						# Colocar uma lampada abaixo do 2
						tab[i + 2][j - 1] = '@'
						# Coloca ruma lampada à esquerda do 2
						tab[i + 1][j - 2] = '@'
				# Se caracter for 1
				if caracter == "1":
					# Se não estivermos na primeira linha nem na primeira coluna e houver um 3 acima à esquerda
					if i > 0 and j > 0 and tab[i - 1][j - 1] == "3":
						# Colocar uma lampada acima do 3
						tab[i - 2][j - 1] = '@'
						# Colocar uma lampada à esquerda do 3
						tab[i - 1][j - 2] = '@'
					# Se não estivermos na primeira linha nem na última coluna e houver um 3 acima à direita
					if i > 0 and j < len(line) - 1 and tab[i - 1][j + 1] == "3":
						# Colocar uma lampada acima do 3
						tab[i - 2][j + 1] = '@'
						# Colocar uma lampada à direita do 3
						tab[i - 1][j + 2] = '@'
					# Se não estivermos na útlima linha, última coluna e houver um 3 abaixo à direita
					if i < len(tab) - 1 and j < len(line) -1 and tab[i + 1][j + 1] == "3":
						# Colocar uma lampada abaixo do 3
						tab[i + 2][j + 1] = '@'
						# Colocar uma lampada à direita do 3
						tab[i + 1][j + 2] = '@'
					# Se não estivermos na última linha, primeira coluna e houver um 3 abaixo à esquerda
					if i < len(tab) - 1 and j > 0 and tab[i + 1][j - 1] == "3":
						# Colocar uma lampada abaixo do 3
						tab[i + 2][j - 1] = '@'
						# Coloca ruma lampada à esquerda do 3
						tab[i + 1][j - 2] = '@'
		return tab

	def do_est5(self, tabuleiro):
		'''comando que permite realizar a estratégia 5 onde colocamos uma lâmpada quando uma casa
		apenas é iluminada se nela estiver uma lâmpada
		parâmetro: tabuleiro
		'''
		tab = copy.deepcopy(tabuleiro)
		# Ciclo para percorrer as linhas do tabuleiro -> retorna cada linha
		for i, line in enumerate(tab):
			# Ciclo para percorrer as colunas da linha retornada -> retorna caracter
			for j, caracter in enumerate(line):
				# Se posição só poder ser iluminada por ela própria
				if eng.so_iluminado_por_ele(tab, i, j):
					# Colocar lá uma lâmpada
					tab[i][j] = '@'
		return tab

	def do_undo(self):
		'''comando que permite desfazer os efeitos do comando anterior
		'''
		return eng.undo()

	def do_resolve(self, tabuleiro):
		'''comando que permite resolver automaticamente o tabuleiro fornecido
		parâmetro: tabuleiro
		'''
		# Cria cópia do tabuleiro
		tab = copy.deepcopy(tabuleiro)
		# Colocar pontos obrigatórios, onde não pode haver lâmpadas
		tab = self.do_est3(tab)
		# Colocar lampadas obrigatórias
		tab = self.do_est4(tab) # Colocar lampadas onde são obrigatórias
		tab = self.do_est5(tab) # Colocar lampadas onde só podem existir lampadas
		# Enquanto houverem casas vazias
		coordenadas = eng.proxima_casa_disponivel(tab)
		while coordenadas != None:
			# Enquanto o tab não se alterar
			anterior = tab
			novo = self.do_est1(anterior) # Se uma casa for N, coloca N lampadas (se visinhança tiver exatamente N casas)
			novo = self.do_est2(novo) # Colocar pontos
			while not eng.tabuleiro_identico(novo, anterior):
				anterior = novo
				novo = self.do_est1(novo) # Se uma casa for N, coloca N lampadas (se visinhança tiver exatamente N casas)
				novo = self.do_est2(novo) # Colocar pontos
			tab = novo
			coordenadas = eng.proxima_casa_disponivel(tab) # (x, y), dá a primrira posição do tabuleiro disponível
			# Se houver uma casa vazia ("-")
			if coordenadas != None:
				# Colocar lá uma lâmpada
				tab[coordenadas[0]][coordenadas[1]] = '@'
		return tab

	def do_ver(self):
		'''comando para visualizar o estado atual do puzzle em ambiente grafico caso seja válido
		'''
		global janela  # pois pretendo atribuir um valor a um identificador global
		if janela is not None:
			del janela  # invoca o metodo destruidor de instancia __del__()
		janela = IlluminatiWindow(40, eng.getlinhas(), eng.getcolunas())
		janela.mostraJanela(eng.gettabuleiro())

	def do_sair(self):
		'''comando para sair do programa
		'''
		print('Obrigado por ter utilizado o illuminati')
		global janela  # pois pretendo atribuir um valor a um identificador global
		if janela is not None:
			del janela
		return True

	def cmdloop(self):
		'''comando que serve como menu para aceder a todas as funções usando uma palavra-chave
		'''
		# Inicializar opção
		option = ""
		# Enquanto opção diferente de "Sair"
		while option != "sair":
			# Ler opção do utilizador
			option = input("Opção: ")
			# "sair".split(" ") => ["sair"]        "mr ficheiro".split(" ") => ["mr", "ficheiro"]
			tokens = option.split()
			command = tokens[0]
			# Executar código correspondente
			if command == "mr":
				self.do_mr(tokens[1])
			elif command == "cr":
				self.do_cr(tokens[1])
			elif command == "gr":
				self.do_gr(tokens[0])
			elif command == "sair":
				self.do_sair()
			else:
				# Se o tabuleiro não estiver carregado, sair
				# os comandos abaixo não fazem sentido se não houver tabuleiro
				if not eng.verifica_tabuleiro():
					print("Um tabuleiro ainda não foi carregado!")
					continue
				if command == "ver":
					self.do_ver()
					continue
				if command == "grh":
					self.do_grh(tokens[1])
					continue
				if command == "undo":
					novo_tabuleiro = self.do_undo()
				else:
					# Vamos buscar o tabuleiro atual
					tabuleiro = eng.gettabuleiro()
					# alterar o tabuleiro consoante a opção
					if command == "jg":
						novo_tabuleiro = self.do_jg(tabuleiro, int(tokens[1]), int(tokens[2]))
					elif command == "mi":
						novo_tabuleiro = self.do_mi(tabuleiro)
					elif command == "est1":
						novo_tabuleiro = self.do_est1(tabuleiro)
					elif command == "est2":
						novo_tabuleiro = self.do_est2(tabuleiro)
					elif command == "est3":
						novo_tabuleiro = self.do_est3(tabuleiro)
					elif command == "est4":
						novo_tabuleiro = self.do_est4(tabuleiro)
					elif command == "est5":
						novo_tabuleiro = self.do_est5(tabuleiro)
					elif command == "resolve":
						novo_tabuleiro = self.do_resolve(tabuleiro)
					# Fazer set do tabulerio (auxiliar) no tabuleiro do IlluminatiEngine (classe)
					eng.settabuleiro(novo_tabuleiro)
				self.print_puzzle(novo_tabuleiro)
				self.do_ver()

if __name__ == '__main__':
	eng = IlluminatiEngine()
	janela = None
	sh = IlluminatiShell()
	sh.cmdloop()
	pass
