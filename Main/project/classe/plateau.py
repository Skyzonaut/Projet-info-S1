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

		# Print la bordure haute
		print("-" * 153)

		# Itère pour chaque ligne de l'échiquier, de haut en bas
		for row in range(1, 9):

			line = ""

			# Itère pour chaque colonne de l'échiquier, de gauche à droite
			for colomn in range(1, 9):

					# Nom (id) de la pièce
					name = self.matrice[(colomn, row)].getName()

					# Ajout de la pièce dans une case qui sera ajoutée à la ligne qui sera affichée plus tard
					line += "|" + self.matrice[(colomn, row)].getName().center(18)


			# Print la ligne et la ferme à droite
			print(line + "|")

			# Print la bordure basse
			print("-" * 153)


	def apercuText(self):

		# Print la bordure haute
		print("-" * 153)

		# Génère et récupère une ligne vide mais coupée par les bords pour servir de partie
		# Des cellules ne contenant pas te texte
		interline = ""
		for i in range(1, 9): interline += "|" + " ".center(18)
		interline += "|"

		# Itère pour chaque ligne de l'échiquier, de haut en bas
		for row in range(1, 9):

			# Print deux lignes d'espace entre le nom de la pièce et le bord haut de la case
			print(interline)
			print(interline)

			line = ""

			# Itère pour chaque colonne de l'échiquier, de gauche à droite
			for colomn in range(1, 9):

					# Nom (id) de la pièce
					name = self.matrice[(colomn, row)].getName()

					# Ajout de la pièce dans une case qui sera ajoutée à la ligne qui sera affichée plus tard
					line += "|" + self.matrice[(colomn, row)].getName().center(18)

			# Print la ligne et la ferme à droite
			print(line + "|")

			# Print deux lignes d'espace entre le nom de la pièce et le bords bas de la case
			print(interline)
			print(interline)

			# Print la bordure basse
			print("-" * 153)



	def reinitialize(self):
		self.__init__()

	def getCase(self, x, y):
		return self.matrice[(x, y)]

# plat = plateau()
# plat.apercu()