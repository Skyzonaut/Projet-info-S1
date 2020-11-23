from tkinter import *
from random import randrange
from pprint import *
from .plateau import *


class pion:

	def __init__(self):

		self.listePions = {}
		#Pions noirs
		for couleur in ["blanc","noir"]:
			for i in range(1,9):
				self.listePions[f"{i}_pion_{couleur}"] = {
					"type" : "pion",
					"couleur" : couleur,
					"state" : True
				}
			for i in range(1,3):
				self.listePions[f"{i}_cavalier_{couleur}"] = {
					"type": "cavalier",
					"couleur": couleur,
					"state" : True
				}
			for i in range(1,3):
				self.listePions[f"{i}_fou_{couleur}"] = {
					"type": "fou",
					"couleur": couleur,
					"state" : True
				}
			self.listePions[f"1_roi_{couleur}"] = {
					"type": "roi",
					"couleur": couleur,
					"state" : True
			}
			self.listePions[f"1_reine_{couleur}"] = {
				"type": "reine",
				"couleur": couleur,
					"state" : True
			}

	def apercu(self):
		pprint(self.listePions)


plateau = plateau()
plateau.apercu()