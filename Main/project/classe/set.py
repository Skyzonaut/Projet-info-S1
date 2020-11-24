from pprint import *
from tkinter import *
from pion import *

class set:

	def __init__(self):

		root = Tk()

		self.listePions = {}

		for couleur in ["blanc","noir"]:
			for i in range(1,9):
				name = f"{i}_pion_{couleur}"
				photo = PhotoImage(file=f"../../../res/{couleur}/pion_{couleur}.png")
				pièce = pion(name, "pion", couleur, True, photo)
				self.listePions[name] = pièce

			for i in range(1,3):
				name = f"{i}_cavalier_{couleur}"
				photo = PhotoImage(file=f"../../../res/{couleur}/cavalier_{couleur}.png")
				pièce = pion(name, "cavalier", couleur, True, photo)
				self.listePions[name] = pièce

			for i in range(1,3):
				name = f"{i}_fou_{couleur}"
				photo = PhotoImage(file=f"../../../res/{couleur}/fou_{couleur}.png")
				pièce = pion(name, "fou", couleur, True, photo)
				self.listePions[name] = pièce

			for i in range(1,3):
				name = f"{i}_tour_{couleur}"
				photo = PhotoImage(file=f"../../../res/{couleur}/tour_{couleur}.png")
				pièce = pion(name, "tour", couleur, True, photo)
				self.listePions[name] = pièce

			name = f"1_reine_{couleur}"
			photo = PhotoImage(file=f"../../../res/{couleur}/reine_{couleur}.png")
			pièce = pion(name, "reine", couleur, True, photo)
			self.listePions[name] = pièce

			name = f"1_roi_{couleur}"
			photo = PhotoImage(file=f"../../../res/{couleur}/roi_{couleur}.png")
			pièce = pion(name, "roi", couleur, True, photo)
			self.listePions[name] = pièce


	"""
	=====================================================================================================
	Fonctions
	=====================================================================================================
	"""

	def getSet(self): return self.listePions

	def apercu(self): pprint(self.listePions)


	def getPion(self, type, couleur):

		listOfMatchingPions = {}

		for pion, att in self.listePions.items():
			if type in pion and couleur in pion:
				listOfMatchingPions[pion] = att

		return listOfMatchingPions



sett = set()
for nom,att in sett.getSet().items():
	att.apercu()
	print("")