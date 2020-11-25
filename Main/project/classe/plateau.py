from .pion import *
from .set import *

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
				pion = self.setDeJeu.getFreePion("empty","")
				self.matrice[(x,y)] = pion

		# ===============================================================================================
		# Blanc
		# ===============================================================================================

		for i in range(1,9):
			pion = self.setDeJeu.getFreePion("pion","noir")
			self.matrice[(2,i)] = pion

		self.matrice[(1, 1)] = self.setDeJeu.getFreePion("tour","noir")
		self.matrice[(1, 2)] = self.setDeJeu.getFreePion("cavalier","noir")
		self.matrice[(1, 3)] = self.setDeJeu.getFreePion("fou","noir")
		self.matrice[(1, 4)] = self.setDeJeu.getFreePion("roi","noir")
		self.matrice[(1, 5)] = self.setDeJeu.getFreePion("reine","noir")
		self.matrice[(1, 6)] = self.setDeJeu.getFreePion("fou","noir")
		self.matrice[(1, 7)] = self.setDeJeu.getFreePion("cavalier","noir")
		self.matrice[(1, 8)] = self.setDeJeu.getFreePion("tour","noir")

		# ===============================================================================================
		# Noir
		# ===============================================================================================

		for i in range(1, 9):
			pion = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(7, i)] = pion

		self.matrice[(8, 1)] = self.setDeJeu.getFreePion("tour","blanc")
		self.matrice[(8, 2)] = self.setDeJeu.getFreePion("cavalier","blanc")
		self.matrice[(8, 3)] = self.setDeJeu.getFreePion("fou","blanc")
		self.matrice[(8, 4)] = self.setDeJeu.getFreePion("roi","blanc")
		self.matrice[(8, 5)] = self.setDeJeu.getFreePion("reine","blanc")
		self.matrice[(8, 6)] = self.setDeJeu.getFreePion("fou","blanc")
		self.matrice[(8, 7)] = self.setDeJeu.getFreePion("cavalier","blanc")
		self.matrice[(8, 8)] = self.setDeJeu.getFreePion("tour","blanc")

	def apercu(self):

		print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")

		for x in range(1, 9):

			line = ""

			for y in range(1, 9):

				name = self.matrice[(x,y)].getName()
				name = name if name != "" else "    "
				line += ("| " + name + " ").ljust(20)

			print(line + "|")

			print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")

	def reinitialize(self):
		self.__init__()

	def getCase(self, x, y):
		return self.matrice[(x, y)]

# plat = plateau()
# plat.apercu()