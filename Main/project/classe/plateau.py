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

		# Matrice contenant les cases et dans ces cases leur contenu
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
			self.matrice[(i,2)] = pion

		self.matrice[(1, 1)] = self.setDeJeu.getFreePion("tour","noir")
		self.matrice[(2, 1)] = self.setDeJeu.getFreePion("cavalier","noir")
		self.matrice[(3, 1)] = self.setDeJeu.getFreePion("fou","noir")
		self.matrice[(4, 1)] = self.setDeJeu.getFreePion("reine","noir")
		self.matrice[(5, 1)] = self.setDeJeu.getFreePion("roi","noir")
		self.matrice[(6, 1)] = self.setDeJeu.getFreePion("fou","noir")
		self.matrice[(7, 1)] = self.setDeJeu.getFreePion("cavalier","noir")
		self.matrice[(8, 1)] = self.setDeJeu.getFreePion("tour","noir")

		# ===============================================================================================
		# Noir
		# ===============================================================================================

		for i in range(1, 9):
			pion = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(i, 7)] = pion

		self.matrice[(1, 8)] = self.setDeJeu.getFreePion("tour","blanc")
		self.matrice[(2, 8)] = self.setDeJeu.getFreePion("cavalier","blanc")
		self.matrice[(3, 8)] = self.setDeJeu.getFreePion("fou","blanc")
		self.matrice[(4, 8)] = self.setDeJeu.getFreePion("reine","blanc")
		self.matrice[(5, 8)] = self.setDeJeu.getFreePion("roi","blanc")
		self.matrice[(6, 8)] = self.setDeJeu.getFreePion("fou","blanc")
		self.matrice[(7, 8)] = self.setDeJeu.getFreePion("cavalier","blanc")
		self.matrice[(8, 8)] = self.setDeJeu.getFreePion("tour","blanc")


	"""
	==================================================================================
	Fonctions
	==================================================================================
	"""


	def moveToAndTake(self, case1, case2):

		piece1 = self.matrice[case1]

		self.matrice[case2].setState(False)
		self.matrice[case2].setAssociation(False)
		self.matrice[case2] = piece1
		self.matrice[case1] = self.setDeJeu.getFreePion("empty","")

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