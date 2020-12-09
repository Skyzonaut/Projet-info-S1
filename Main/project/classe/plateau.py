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
		Création du plateau
		==============================================================================
		"""

		# Matrice contenant les cases et dans ces cases leur contenu
		self.matrice = {}

		# ===============================================================================================
		# Cases vides du milieu du plateau
		# ===============================================================================================

		for y in range(3,7):
			for x in range(1, 9):
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


	def move(self, origin: tuple, destination: tuple) -> None:
		"""

		:param origin: tuple of int *Case de départ*
		:param destination: tuple of int *Case d'arrivé*
		:return: None

		Fonction qui permet de bouger un pion, et gère plusieurs cas :
			- Origin == Destination *Clique sur la même case* : Ne fait rien
			- Destination == Empty *Déplace sur une case vide* : Interchange le pion et la case vide
			- Destination == pion *Déplace sur un case pleine et prend le pion* : Se déplace, et retire le pion du plateau, passe son état à False

		"""

		# Si le joueur ne reclique pas sur la meme case, dans le cas donc faire un déplacement
		if origin != destination:

			# Si cette case n'est pas vide
			if not "empty" in self.getCase(destination[0], destination[1]).getName():

				# On retire le pion qui va être prit du jeu en passant son état à False
				self.matrice[(destination[0], destination[1])].setState(False)

				# On met le pion de la case d'origine à la place du pion d'arrivé
				self.setCase(destination[0], destination[1], self.getCase(origin[0], origin[1]))

				# On vide la case de départ avec la fonction empty(), qui y rajoute un pion vide
				self.empty(origin[0], origin[1])

			# Si la case est vide, on se contente d'interchanger les cases, la vide devient la pleine et vis et versa
			else:

				# On récupère les pions pour pas s'embrouiller à cause de l'ordre d'association des variables
				pionOrigin = self.getCase(origin[0], origin[1])
				pionDestination = self.getCase(destination[0], destination[1])

				# On échange les cases
				self.setCase(origin[0], origin[1], pionDestination)
				self.setCase(destination[0], destination[1], pionOrigin)

		# Si le joueur reclique sur la meme case
		else:

			pass


	def empty(self, x, y):
		self.matrice[(x, y)] = self.setDeJeu.getFreePion("empty","")

	def reinitialize(self):
		self.__init__()

	def getCase(self, x, y):
		return self.matrice[(x, y)]

	def setCase(self, x, y, content):
		self.matrice[(x, y)] = content

	def apercuSet(self):
		self.setDeJeu.apercu()

	def apercu(self):

		# Print la bordure haute
		print("-" * 153)

		# Itère pour chaque ligne de l'échiquier, de haut en bas
		for row in range(1, 9):

			line = ""

			# Itère pour chaque colonne de l'échiquier, de gauche à droite
			for colomn in range(1, 9):

					# Si la case est censée être vide, on ajoute un blanc à la ligne qui sera affiché plus tard
					if not self.matrice[(colomn, row)]:
						line += "|" + "".center(18)

					# Ajout de la pièce dans une case qui sera ajoutée à la ligne qui sera affichée plus tard
					else:
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


	"""
	==================================================================================
	RULES
	==================================================================================
	"""

	def getPath(self, origin: tuple) -> list:
		"""

		:param origin: tuple of int *Case*
		:return: list of tuple of int *Liste des cases où peut bouger le pion*

		Fonction récupérant le plateau à l'état actuel, le pion à bouger, et renvoie toutes les cas sur lesquelles il peut se déplacer.
		S'arrête toujours au premier pion adversaire pris, et gère la colision avec les pions alliés
		"""









