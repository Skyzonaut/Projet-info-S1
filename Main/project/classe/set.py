from pprint import *
from tkinter import *
from .pion import *

class set:

	def __init__(self):

		root = Tk(className="Remerciement")

		self.listePions = {}

		for couleur in ["blanc","noir"]:

			for i in range(1,9):
				name = f"{i}_pion_{couleur}"
				photo = PhotoImage(file=f"../res/{couleur}/pion_{couleur}.png")
				piece = pion(name, "pion", couleur, False, photo)
				self.listePions[name] = piece

			for i in range(1,3):
				name = f"{i}_cavalier_{couleur}"
				photo = PhotoImage(file=f"../res/{couleur}/cavalier_{couleur}.png")
				piece = pion(name, "cavalier", couleur, False, photo)
				self.listePions[name] = piece

			for i in range(1,3):
				name = f"{i}_fou_{couleur}"
				photo = PhotoImage(file=f"../res/{couleur}/fou_{couleur}.png")
				piece = pion(name, "fou", couleur, False, photo)
				self.listePions[name] = piece

			for i in range(1,3):
				name = f"{i}_tour_{couleur}"
				photo = PhotoImage(file=f"../res/{couleur}/tour_{couleur}.png")
				piece = pion(name, "tour", couleur, False, photo)
				self.listePions[name] = piece

			name = f"1_reine_{couleur}"
			photo = PhotoImage(file=f"../res/{couleur}/reine_{couleur}.png")
			piece = pion(name, "reine", couleur, False, photo)
			self.listePions[name] = piece

			name = f"1_roi_{couleur}"
			photo = PhotoImage(file=f"../res/{couleur}/roi_{couleur}.png")
			piece = pion(name, "roi", couleur, False, photo)
			self.listePions[name] = piece

			for i in range(1,66):
				name = f"{i}_empty"
				piece = pion(name, "", "", False, None)
				self.listePions[name] = piece

		root.destroy()

	"""
	=====================================================================================================
	Fonctions
	=====================================================================================================
	"""

	def getSet(self): return self.listePions

	def apercu(self):
		for name, pion in self.listePions.items():
			print("{")
			pion.apercu()
			print("},")

	def getPions(self, type, couleur):

		listOfMatchingPions = {}

		for pion, att in self.listePions.items():
			if type in pion and couleur in pion:
				listOfMatchingPions[pion] = att

		return listOfMatchingPions


	def getFreePion(self, type, couleur):

		for name, pion in self.listePions.items():

			if type in name and couleur in name and not pion.getState():

				self.listePions[name].setState(True)

				return pion

		return None

# sette = set()
# sette.apercu()