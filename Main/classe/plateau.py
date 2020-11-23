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
				self.matrice[(x,y)] = {"content":" ","fond":""}

		#Blanc
		for i in range(1,9): self.matrice[(2,i)] = {"content":"P","fond":""};
		self.matrice[(1, 1)] = {"content": "T", "fond": ""}
		self.matrice[(1, 2)] = {"content": "C", "fond": ""}
		self.matrice[(1, 3)] = {"content": "F", "fond": ""}
		self.matrice[(1, 4)] = {"content": "R", "fond": ""}
		self.matrice[(1, 5)] = {"content": "K", "fond": ""}
		self.matrice[(1, 6)] = {"content": "F", "fond": ""}
		self.matrice[(1, 7)] = {"content": "C", "fond": ""}
		self.matrice[(1, 8)] = {"content": "T", "fond": ""}

		#Noir
		for i in range(1,9): self.matrice[(7,i)] = {"content":"p","fond":""};
		self.matrice[(8, 1)] = {"content": "t", "fond": ""}
		self.matrice[(8, 2)] = {"content": "c", "fond": ""}
		self.matrice[(8, 3)] = {"content": "f", "fond": ""}
		self.matrice[(8, 4)] = {"content": "r", "fond": ""}
		self.matrice[(8, 5)] = {"content": "k", "fond": ""}
		self.matrice[(8, 6)] = {"content": "f", "fond": ""}
		self.matrice[(8, 7)] = {"content": "c", "fond": ""}
		self.matrice[(8, 8)] = {"content": "t", "fond": ""}




	def apercu(self):
		print("-------------------------------------------------")
		for x in range(1, 9):
			line = "|"
			for y in range(1, 9):
				line += "  " + self.matrice[(x,y)]["content"] + "  |"
			print(line)
			print("-------------------------------------------------")
		pass



plateau = plateau()
pprint(plateau.matrice)
plateau.apercu()