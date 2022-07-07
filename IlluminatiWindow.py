# -*- coding:utf-8 -*-

from graphics import *
from tkinter.constants import CENTER

class IlluminatiWindow:

    '''
    Classe que cria uma janela para vizualização grafica do estado de um tabuleiro
    '''
    def __init__(self, cell_size, linhas, colunas):
        '''
        Cria nova instancia de IlluminatiPrinter
        :param cell_size: tamanho da casa no ecra, em pixeis
        :param filename: nome do ficheiro a ler
        '''
        self.cell_size = cell_size
        self.nlinhas = linhas
        self.ncolunas = colunas
        self.puzzle = GraphWin("Illuminati", self.nlinhas * self.cell_size + self.cell_size, self.ncolunas * self.cell_size + self.cell_size)
        pass


    def __del__(self):
        self.puzzle.close()  # fechar a janela


    def desenhaCasa(self, coluna, linha):
        '''
        Desenha uma casa vazia
        :param coluna: indice da coluna
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        Rectangle(p1, p2).draw(self.puzzle)

    def desenhaCasaIluminada(self, coluna, linha):
        '''
        Desenha uma casa que esteja iluminada mas nao contenha lampada
        :param coluna: indice da coluna
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("#%02x%02x%02x" % (255, 247, 162))  # cor RGB da luz
        r.draw(self.puzzle)

    def desenhaLampada(self, coluna, linha):
        '''
        Desenha uma casa que contenha lampada
        :param coluna: indice da coluna
        :param linha: indice da linha
        '''
        self.desenhaCasaIluminada(coluna, linha)

        p1 = Point(coluna * self.cell_size + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2)
        c = Circle(p1, self.cell_size / 3)
        c.setFill("yellow")
        c.draw(self.puzzle)

    def desenhaCasaBloqueada(self, coluna, linha):
        '''
        Desenha uma casa que esteja bloqueada sem conter qualquer numero
        :param coluna: indice da coluna
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("black")
        r.draw(self.puzzle)
        return r

    def desenhaCasaBloqueadaNum(self, coluna, linha, char):
        '''
        Desenha uma casa que esteja bloqueada e contenha um numero
        :param coluna: indice da coluna
        :param linha: indice da linha
        :param char: caracter numerico a inserir na casa bloqueada
        '''
        r = self.desenhaCasaBloqueada(coluna, linha)  # aqui aproveitamos o retangulo que definimos para lhe colocar texto centrado

        label = Text(r.getCenter(), char)
        label.setTextColor("white")
        label.draw(self.puzzle)

    def desenhaCasaMarcada(self, coluna, linha):
        '''
        Desenha uma casa que esteja marcada como nao podendo conter uma lampada
        :param coluna: indice da coluna
        :param linha: indice da linha
        '''
        self.desenhaCasa(coluna, linha)
        p1 = Point(coluna * self.cell_size + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2)

        c = Circle(p1, self.cell_size / 10)
        c.setFill("black")
        c.draw(self.puzzle)

    def desenhaNumLinha(self, linha):
        label = Text(Point(0 + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2), str(linha))
        label.setTextColor("black")
        label.draw(self.puzzle)

    def desenhaNumsColunas(self, colunas):
        for i in range(1, colunas + 1):
            label = Text(Point(i * self.cell_size + self.cell_size / 2 , self.cell_size / 2), str(i))
            label.setTextColor("black")
            label.draw(self.puzzle)


    def mostraJanela(self, matriz):
        '''
        Percorre todo o puzzle, linha a linha e dentro de cada linha coluna a coluna, desenhando cada casa correspondente no puzzle
        '''
        self.puzzle.delete("all")
        linha = 0
        coluna = 0
        self.desenhaNumsColunas(self.ncolunas)
        for line in matriz:
            for column in line:
                self.desenhaNumLinha(linha + 1)
                if column == '-':
                    self.desenhaCasa(coluna + 1, linha + 1)
                elif column == 'x':
                    self.desenhaCasaBloqueada(coluna + 1, linha + 1)
                elif column == '@':
                    self.desenhaLampada(coluna + 1, linha + 1)
                elif column == 'o':
                    self.desenhaCasaIluminada(coluna + 1, linha + 1)
                elif column == '.':
                    self.desenhaCasaMarcada(coluna + 1, linha + 1)
                else:
                    self.desenhaCasaBloqueadaNum(coluna + 1, linha + 1, column)
                coluna = coluna + 1
            coluna = 0
            linha = linha + 1


