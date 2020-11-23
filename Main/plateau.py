from tkinter import *
from random import randrange
from pprint import *


class plateau:

	def __init__(self):

		#Creation du plateau

		self.matrice = {}

		for x in range(1,9):
			for y in range(1,9):
				self.matrice[(x,y)] = ""

		def apercu():
			final = ""
			for x in range(1, 9):
				line = "|"
				for y in range(1, 9):
					line += " " + self.matrice[(x,y)] + " |"
				final += line+'\n'
			return final

plateau = plateau()
pprint(plateau.matrice)
plateau.apercu()