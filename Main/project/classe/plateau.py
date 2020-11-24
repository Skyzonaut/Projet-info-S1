from pion import *
from set import *

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

		#Récupération de tous les pions
		self.setDeJeu = set()

		"""
		==============================================================================
		Création du palteau
		==============================================================================
		"""

		self.matrice = {}
		for x in range(1,9):
			for y in range(1,9):
				self.matrice[(x,y)] = {"content":	" ","fond":""}

		#Blanc
		for i in range(1,9):
			pion = self.setDeJeu.getFreePion("pion","noir")
			print(pion.getName())
			self.matrice[(2,i)] = {"content": pion, "fond": ""}

		self.matrice[(1, 1)] = {"content": self.setDeJeu.getFreePion("tour","noir"), "fond": ""}
		self.matrice[(1, 2)] = {"content": self.setDeJeu.getFreePion("cavalier","noir"), "fond": ""}
		self.matrice[(1, 3)] = {"content": self.setDeJeu.getFreePion("fou","noir"), "fond": ""}
		self.matrice[(1, 4)] = {"content": self.setDeJeu.getFreePion("reine","noir"), "fond": ""}
		self.matrice[(1, 5)] = {"content": self.setDeJeu.getFreePion("roi","noir"), "fond": ""}
		self.matrice[(1, 6)] = {"content": self.setDeJeu.getFreePion("fou","noir"), "fond": ""}
		self.matrice[(1, 7)] = {"content": self.setDeJeu.getFreePion("cavalier","noir"), "fond": ""}
		self.matrice[(1, 8)] = {"content": self.setDeJeu.getFreePion("tour","noir"), "fond": ""}

		#Noir
		for i in range(1,9): self.matrice[(7,i)] = {"content":"p","fond":""};
		self.matrice[(8, 1)] = {"content": self.setDeJeu.getFreePion("tour","blanc"), "fond": ""}
		self.matrice[(8, 2)] = {"content": self.setDeJeu.getFreePion("cavalier","blanc"), "fond": ""}
		self.matrice[(8, 3)] = {"content": self.setDeJeu.getFreePion("fou","blanc"), "fond": ""}
		self.matrice[(8, 4)] = {"content": self.setDeJeu.getFreePion("roi","blanc"), "fond": ""}
		self.matrice[(8, 5)] = {"content": self.setDeJeu.getFreePion("reine","blanc"), "fond": ""}
		self.matrice[(8, 6)] = {"content": self.setDeJeu.getFreePion("fou","blanc"), "fond": ""}
		self.matrice[(8, 7)] = {"content": self.setDeJeu.getFreePion("cavalier","blanc"), "fond": ""}
		self.matrice[(8, 8)] = {"content": self.setDeJeu.getFreePion("tour","blanc"), "fond": ""}


	def apercu(self):
		print("-------------------------------------------------")
		for x in range(1, 9):
			line = "|"
			for y in range(1, 9):
				line += "  " + self.matrice[(x,y)]["content"].getName() + "  |"
			print(line)
			print("-------------------------------------------------")

	def reinitialize(self):
		self.__init__()

# plat = plateau()
# plat.apercu()