from tkinter import *
from random import randrange
from pprint import *


class plateau:

	"""
	Dictionnaire de type:
	{ (x,y) : {
		'content' : 'Pion',
		'fond' : 'UrlImageDuPion'
		}
	}
	"""
	def __init__(self):

		#Création du tableau
		self.matrice = {}
		for x in range(1,9):
			for y in range(1,9):
				if x == 5:
					self.matrice[(x,y)] = {"content":"X","fond":"../res/black_tower.png"}
				else:
					self.matrice[(x,y)] = {"content":"","fond":""}


	def apercu(self):
		for x in range(1, 9):
			line = "|"
			for y in range(1, 9):
				line += "  " + self.matrice[(x,y)]["content"] + "  |"
			print("-------------------------------------------------")
			print(line)
		pass



plateau = plateau()
pprint(plateau.matrice)
plateau.apercu()