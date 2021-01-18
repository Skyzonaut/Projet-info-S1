from .pion import *
from .set import *
from math import *

class Plateau:

	"""
	Dictionnaire de type:
	{ (x,y) : {
		'content' : 'Pion',
		'fond' : 'UrlImageDuPion'
		}
	}
	"""
	def __init__(self, initType: str):
		"""
		Objet contenant une matrice quadrillant un jeu d'echec et stockant le contenu des cases.

		:param initType: "classic" = déploiement classic | "other" = déploiement spécifique
		"""
		# écupération de tous les pions
		self.setDeJeu = set()

		"""
		==============================================================================
		Création du plateau
		==============================================================================
		"""

		# Matrice contenant les cases et dans ces cases leur contenu
		self.matrice = {}

		# Initialisation normale si indiqué dans le constructeur via la paramètre initType
		if initType == "classic":

			# ===============================================================================================
			# Cases vides du milieu du plateau
			# ===============================================================================================

			for y in range(3, 7):
				for x in range(1, 9):
					newPion = self.setDeJeu.getFreePion("empty", "")
					self.matrice[(x, y)] = newPion

			# ===============================================================================================
			# Blanc
			# ===============================================================================================

			for i in range(1, 9):
				newPion = self.setDeJeu.getFreePion("pion", "noir")
				self.matrice[(i, 2)] = newPion

			self.matrice[(1, 1)] = self.setDeJeu.getFreePion("tour", "noir")
			self.matrice[(2, 1)] = self.setDeJeu.getFreePion("cavalier", "noir")
			self.matrice[(3, 1)] = self.setDeJeu.getFreePion("fou", "noir")
			self.matrice[(4, 1)] = self.setDeJeu.getFreePion("reine", "noir")
			self.matrice[(5, 1)] = self.setDeJeu.getFreePion("roi", "noir")
			self.matrice[(6, 1)] = self.setDeJeu.getFreePion("fou", "noir")
			self.matrice[(7, 1)] = self.setDeJeu.getFreePion("cavalier", "noir")
			self.matrice[(8, 1)] = self.setDeJeu.getFreePion("tour", "noir")

			# ===============================================================================================
			# Noir
			# ===============================================================================================

			for i in range(1, 9):
				newPion = self.setDeJeu.getFreePion("pion", "blanc")
				self.matrice[(i, 7)] = newPion

			self.matrice[(1, 8)] = self.setDeJeu.getFreePion("tour", "blanc")
			self.matrice[(2, 8)] = self.setDeJeu.getFreePion("cavalier", "blanc")
			self.matrice[(3, 8)] = self.setDeJeu.getFreePion("fou", "blanc")
			self.matrice[(4, 8)] = self.setDeJeu.getFreePion("reine", "blanc")
			self.matrice[(5, 8)] = self.setDeJeu.getFreePion("roi", "blanc")
			self.matrice[(6, 8)] = self.setDeJeu.getFreePion("fou", "blanc")
			self.matrice[(7, 8)] = self.setDeJeu.getFreePion("cavalier", "blanc")
			self.matrice[(8, 8)] = self.setDeJeu.getFreePion("tour", "blanc")

		# Initialisation différente si indiqué dans le constructeur via la paramètre initType
		elif initType == "other":

			self.matrice[(1, 2)] = self.setDeJeu.getFreePion("pion", "noir")
			self.matrice[(2, 2)] = self.setDeJeu.getFreePion("pion", "noir")
			self.matrice[(3, 2)] = self.setDeJeu.getFreePion("pion", "noir")
			self.matrice[(6, 2)] = self.setDeJeu.getFreePion("pion", "noir")
			self.matrice[(7, 2)] = self.setDeJeu.getFreePion("pion", "noir")
			self.matrice[(8, 4)] = self.setDeJeu.getFreePion("pion", "noir")

			self.matrice[(4, 5)] = self.setDeJeu.getFreePion("cavalier", "noir")
			self.matrice[(2, 3)] = self.setDeJeu.getFreePion("fou", "noir")
			self.matrice[(3, 5)] = self.setDeJeu.getFreePion("reine", "noir")
			self.matrice[(2, 1)] = self.setDeJeu.getFreePion("roi", "noir")
			self.matrice[(7, 3)] = self.setDeJeu.getFreePion("fou", "noir")

			# ===============================================================================================
			# Noir
			# ===============================================================================================

			self.matrice[(1, 7)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(2, 7)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(3, 7)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(5, 4)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(6, 5)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(7, 4)] = self.setDeJeu.getFreePion("pion", "blanc")
			self.matrice[(8, 5)] = self.setDeJeu.getFreePion("pion", "blanc")

			self.matrice[(4, 8)] = self.setDeJeu.getFreePion("tour", "blanc")
			self.matrice[(7, 6)] = self.setDeJeu.getFreePion("cavalier", "blanc")
			self.matrice[(5, 6)] = self.setDeJeu.getFreePion("fou", "blanc")
			self.matrice[(3, 8)] = self.setDeJeu.getFreePion("reine", "blanc")
			self.matrice[(2, 8)] = self.setDeJeu.getFreePion("roi", "blanc")

			for x in range(1, 9):
				for y in range(1, 9):
					if not (x,y) in list(self.matrice.keys()):
						self.matrice[(x, y)] = self.setDeJeu.getFreePion("empty", "")

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
			- Destination == pion *Déplace sur un case pleine et prend le pion* :
			Se déplace, et retire le pion du plateau, passe son état à False
		"""

		# Si le joueur ne reclique pas sur la meme case, dans le cas donc faire un déplacement
		if origin != destination:

			# Si cette case n'est pas vide
			if "empty" not in self.getCase(destination[0], destination[1]).getName():

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


	def empty(self, x: int, y: int):
		"""
		Vide une case (x, y)

		:param x: x
		:param y: y
		"""
		self.matrice[(x, y)] = self.setDeJeu.getFreePion("empty", "")


	def getMatrice(self):
		"""
		Retourne le dictionnaire servant de base de donné au plateau

		:return: plateau.matrice
		"""
		return self.matrice


	def getMatriceByCouleur(self, couleur: str):
		"""
		Retourne tous les pions de la couleur précisée

		:param couleur: couleur à récuperer
		:return: plateau.matrice by couleur
		"""

		returnDict = []

		for coordPion, pion in self.matrice.items():

			if pion.getCouleur() == couleur:

				returnDict.append(coordPion)

		return returnDict


	def getCase(self, x, y) -> pion:
		"""
		Récupère le contenu d'une case de coordonnées (x, y) données.

		:param x: x
		:param y: y
		:return: pion
		"""

		return self.matrice[(x, y)]

	def getCaseTuple(self, tuple) -> pion:
		"""
		Récupère le cotenu d'une case de coordonnées (x, y) données.
		Semblable à la fonction getCase(), mais le paramètre est un tuple ici et non deux entiers

		:param tuple: coordonnées
		:return: pion
		"""

		return self.matrice[tuple[0], tuple[1]]

	def setCase(self, x, y, content):
		"""
		Remplace le cotenu d'une case de coordonnées (x, y) données par le pion donné.

		:param tuple: coordonnées
		:param content: pion par lequel remplacer le contenu initial de la case (x, y)
		"""

		self.matrice[(x, y)] = content

	def getRoi(self, couleur: str) -> tuple:
		"""
		Récupère la position du roi de la couleur donnée

		Args:
			couleur: Couleur du roi à chercher. "noir" ou "blanc"

		:return: Coordonnées du roi
		"""

		for coord, pion in self.matrice.items():

			if pion.getType() == "roi" and pion.getCouleur() == couleur:

				return coord


	def pathFinding(self, origin: tuple, target: tuple, takeOrigin=False):
		"""
		Récupère la trajectoire entre une pièce @origin et une pièce @target, stocké en case de différence.

		Ex : (-1,-2) -> (Une case à gauche, Deux case vers le haut)

		Args:
			origin: Pièce d'où part le pathfinding
			target: Pièce qu'il doit atteindre
			takeOrigin: Si la trajectoire doit inclure la pièce à atteindre

		:return: list[tuple]
		"""

		listPathBetween = []

		xOrigin = origin[0]
		yOrigin = origin[1]
		xTarget = target[0]
		yTarget = target[1]

		highestScoreMove = []
		plusOrigin = 0 if not takeOrigin else 1

		if xOrigin == xTarget:
			yDistance = yOrigin - yTarget
			for y in range(1, abs(yDistance) + plusOrigin):
				if yDistance > 0:
					highestScoreMove.append((0, y))
				else:
					highestScoreMove.append((0, -y))

		if yOrigin == yTarget:
			xDistance = xOrigin - xTarget
			for x in range(1, abs(xDistance) + plusOrigin):
				if xDistance > 0:
					highestScoreMove.append((x, 0))
				else:
					highestScoreMove.append((-x, 0))

		xDistance = xOrigin - xTarget
		yDistance = yOrigin - yTarget

		if abs(xDistance) == abs(yDistance):
			negX = 0
			negY = 0

			if xDistance > 0 and yDistance > 0:
				negX = 1
				negY = 1

			elif xDistance > 0 and yDistance < 0:
				negX = 1
				negY = -1

			elif xDistance < 0 and yDistance < 0:
				negX = -1
				negY = -1

			elif xDistance < 0 and yDistance > 0:
				negX = -1
				negY = 1

			for xy in range(1, abs(xDistance) + plusOrigin):
				highestScoreMove.append((xy*negX, xy*negY))

		return highestScoreMove


	def getCasePathFinding(self, origin: tuple, target: tuple, takeOrigin=False):
		"""
		Récupère les cases sur la trajectoire entre une case @origin et une case @target.

		Args:
			origin: Pièce d'où part le pathfinding
			target: Pièce qu'il doit atteindre
			takeOrigin: True si la trajectoire doit contenir la @target (cible), False si elle doit s'arrêter avant

		:returns: Liste des cases sur le trajet
		"""

		listPathFinding = self.pathFinding(origin, target, takeOrigin)
		listCasePathFinding = []

		for path in listPathFinding:

			listCasePathFinding.append((path[0] + target[0], path[1] + target[1]))

		return listCasePathFinding


	def checkEchec(self, couleur: str):
		"""
		Récupère les pions mettant en échec le roi de couleur @couleur

		:param couleur: couleur du roi qui serait mis en échec
		:return: liste des pions qui mettent le roi de la couleur donnée en échec
		"""

		listPieceEchec = []
		ennemiCouleur = "blanc" if couleur == "noir" else "noir"
		coordRoi = self.getRoi(couleur)

		for coordPion in self.getMatriceByCouleur(ennemiCouleur):

			if coordRoi in self.getPath(coordPion):

				listPieceEchec.append(coordPion)

		return listPieceEchec


	def checkMate(self, couleur):
		"""
		Test si le roi de la couleur données est :
			- En echec et mat
			- En echec simple : Dans quel cas retourne la liste des déplacements pouvant sauver le roi
			- Ne retourne rien si aucun des deux précédents

		:param couleur: couleur du roi qui serait mis en échec
		:return: liste des pions qui mettent le roi de la couleur donnée en échec
		"""

		if self.checkEchec(couleur):

			roi = self.getRoi(couleur)
			ennemiCouleur = "blanc" if couleur == "noir" else "noir"
			listePieceAllie = self.getMatriceByCouleur(couleur)
			listePieceEnnemie = self.getMatriceByCouleur(ennemiCouleur)
			listeMovePieceEnnemie = []
			listePieceEchec = []
			listeMoveRoiSave = []

			# On stocke toutes les cases sur le chemin d'un ennemi
			for pieceEnnemie in listePieceEnnemie:

				piecePath = self.getPath(pieceEnnemie, goThrough=True, takeFriends=False)

				if roi in piecePath:

					listePieceEchec.append(pieceEnnemie)

				for casePath in piecePath:

					if casePath not in listeMovePieceEnnemie:

						listeMovePieceEnnemie.append(casePath)

			# On stocke toutes les cases qui sont protégées par un ennemie
			listeMovePieceEnnemieTakeFriends = []

			for pieceEnnemie in listePieceEnnemie:

				piecePath = self.getPath(pieceEnnemie, goThrough=True, takeFriends=True)

				for casePath in piecePath:

					if casePath not in listeMovePieceEnnemieTakeFriends:

						listeMovePieceEnnemieTakeFriends.append(casePath)

			# S'il existe des pièces mettant le roi en echec
			if listeMovePieceEnnemie:

				listeMoveRoi = self.getPath(roi)

				# On récupère les dépalcement du roi, s'il n'est pas sur le chemin d'un ennemi
				for casePathRoi in listeMoveRoi:

					if casePathRoi not in listeMovePieceEnnemieTakeFriends:

						listeMoveRoiSave.append((roi, casePathRoi))

				# Pour chaque pièce mettant le roi en echec, on regarde si le roi peut l'éviter, ou si un autre pion
				# allié peut s'interposer ou si les deux peuvent le prendre.
				for pieceEchec in listePieceEchec:

					for pieceSauveteur in listePieceAllie:

						for movePieceSauveteur in self.getPath(pieceSauveteur):

							# Le roi a déjà été géré alors on l'ignore
							if self.getCaseTuple(pieceSauveteur).getType() != "roi":

								# Si c'est un cavalier il peut éviter des cases
								if self.getCaseTuple(pieceEchec).getType() == "cavalier":

									if movePieceSauveteur == pieceEchec:

										listeMoveRoiSave.append((pieceSauveteur, movePieceSauveteur))

								else:

									if movePieceSauveteur in self.getCasePathFinding(pieceEchec, roi, True):

										listeMoveRoiSave.append((pieceSauveteur, movePieceSauveteur))

				if listeMoveRoiSave:

					return listeMoveRoiSave

				else:

					return "mat"

		else:

			return "no-echec"


	def apercuSet(self):
		"""
		Print sur le terminal l'état du de jeu à l'état actuel.
		"""

		self.setDeJeu.apercu()


	def apercu(self):
		"""
		Affiche sur le terminal un plateau en ASCII contenant et affichant les pions du plateau à l'état actuel
		"""

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
		"""
		Affiche sur le terminal un plateau en ASCII contenant et affichant les pions du plateau à l'état actuel.
		Semblable à apercu() mais ici les cases sont carrées.
		Cela prend plus de place mais ressemble davantage à un vrai échiquier
		"""

		# Print la bordure haute
		print("-" * 153)

		# Génère et récupère une ligne vide mais coupée par les bords pour servir de partie
		# Des cellules ne contenant pas te texte
		interline = ""

		for i in range(1, 9):
			interline += "|" + " ".center(18)

		interline += "|"

		# Itère pour chaque ligne de l'échiquier, de haut en bas
		for row in range(1, 9):

			# Print deux lignes d'espace entre le nom de la pièce et le bord haut de la case
			print(interline)
			print(interline)

			line = ""

			# Itère pour chaque colonne de l'échiquier, de gauche à droite
			for colomn in range(1, 9):

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

	def getPath(self, origin: tuple, goThrough=False, takeFriends=False, pion=False) -> list:
		"""
		:param origin: tuple of int *Case*
		:param goThrough: True si le trajet doit être calculé en ignorant les pions sur sont chemin
		:type goThrough: bool
		:param takeFriends: True si le trajet doit comprendre les alliées du pion
		:type takeFriends: bool
		:param pion: True si le trajet doit afficher les prises d'un pion même si aucun pion ennemi ne permet se move
		:type pion: bool
		:return: list of tuple of int *Liste des cases où peut bouger le pion*

		Fonction qui renvoie toutes les cases sur lesquelles il peut se déplacer selon les paramètres donnés.
		"""

		pionSelected = self.getCase(origin[0], origin[1])

		listPossibleMove = []

		# ==============================================================================================================
		# PION
		# ==============================================================================================================

		if pionSelected.getType().lower() == "pion" and not goThrough and not pion:

			left = -1
			right = +1
			stay = 0

			if pionSelected.getCouleur() == "noir":

				fw = +1

				if origin[1] == 8:

					return listPossibleMove

				if "empty" in self.getCase(origin[0], origin[1] + fw).getName():

					if origin[1] == 2 and "empty" in self.getCase(origin[0], origin[1] + 2*fw).getName():

						listPossibleMove = [(origin[0] + stay, origin[1] + fw), (origin[0] + stay, origin[1] + (2*fw))]

					else:

						listPossibleMove = [(origin[0] + stay, origin[1] + fw)]

				if 0 < origin[0] + left < 9:

					if "empty" not in self.getCase(origin[0] + left , origin[1] + fw).getName() \
						and self.getCase(origin[0] + left , origin[1] + fw).getCouleur() != pionSelected.getCouleur():

						listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					if "empty" not in self.getCase(origin[0] + right, origin[1] + fw).getName() \
						and self.getCase(origin[0] + right, origin[1] + fw).getCouleur() != pionSelected.getCouleur():

						listPossibleMove.append((origin[0] + right, origin[1] + fw))

			elif pionSelected.getCouleur() == "blanc":

				fw = -1

				if origin[1] == 1:

					return listPossibleMove

				if "empty" in self.getCase(origin[0], origin[1] + fw).getName():

					if origin[1] == 7 and "empty" in self.getCase(origin[0], origin[1] + 2*fw).getName():

						listPossibleMove = [(origin[0] + stay, origin[1] + fw), (origin[0] + stay, origin[1] + (2*fw))]

					else:

						listPossibleMove = [(origin[0] + stay, origin[1] + fw)]

				if 0 < origin[0] + left < 9:

					if "empty" not in self.getCase(origin[0] + left, origin[1] + fw).getName() \
						and self.getCase(origin[0] + left, origin[1] + fw).getCouleur() != pionSelected.getCouleur():

						listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					if "empty" not in self.getCase(origin[0] + right, origin[1] + fw).getName() \
						and self.getCase(origin[0] + right, origin[1] + fw).getCouleur() != pionSelected.getCouleur():

						listPossibleMove.append((origin[0] + right, origin[1] + fw))

		elif pionSelected.getType().lower() == "pion" and goThrough and not pion:

			left = -1
			right = +1
			stay = 0

			if pionSelected.getCouleur() == "noir":

				fw = +1

				if origin[1] == 8:

					return listPossibleMove

				if "empty" in self.getCase(origin[0], origin[1] + fw).getName():

					if origin[1] == 2 and "empty" in self.getCase(origin[0], origin[1] + 2 * fw).getName():

						listPossibleMove = [(origin[0] + stay, origin[1] + fw),
											(origin[0] + stay, origin[1] + (2 * fw))]

					else:

						listPossibleMove = [(origin[0] + stay, origin[1] + fw)]

				if 0 < origin[0] + left < 9:

					listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					listPossibleMove.append((origin[0] + right, origin[1] + fw))

			elif pionSelected.getCouleur() == "blanc":

				fw = -1

				if origin[1] == 1:

					return listPossibleMove

				if "empty" in self.getCase(origin[0], origin[1] + fw).getName():

					if origin[1] == 7 and "empty" in self.getCase(origin[0], origin[1] + 2 * fw).getName():

						listPossibleMove = [(origin[0] + stay, origin[1] + fw),
											(origin[0] + stay, origin[1] + (2 * fw))]

					else:

						listPossibleMove = [(origin[0] + stay, origin[1] + fw)]

				if 0 < origin[0] + left < 9:

					listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					listPossibleMove.append((origin[0] + right, origin[1] + fw))

		elif pionSelected.getType().lower() == "pion" and not goThrough and pion:


			left = -1
			right = +1
			stay = 0

			if pionSelected.getCouleur() == "noir":

				fw = +1

				if origin[1] == 1:
					return listPossibleMove

				if 0 < origin[0] + left < 9:
					listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					listPossibleMove.append((origin[0] + right, origin[1] + fw))

			if pionSelected.getCouleur() == "blanc":

				fw = -1

				if origin[1] == 1:

					return listPossibleMove

				if 0 < origin[0] + left < 9:

					listPossibleMove.append((origin[0] + left, origin[1] + fw))

				if 0 < origin[0] + right < 9:

					listPossibleMove.append((origin[0] + right, origin[1] + fw))

		# ==============================================================================================================
		# CAVALIER
		# ==============================================================================================================

		elif pionSelected.getType() == "cavalier":

			for x in [-2, -1, 1, 2]:

				if abs(x) == 1:

					y, my = 2, -2

					if 0 < origin[0] + x < 9:

						if 0 < origin[1] + y < 9:

							if "empty" in self.getCase(origin[0] + x, origin[1] + y).getName():

								listPossibleMove.append((origin[0] + x, origin[1] + y))

							else:

								if not takeFriends:

									if self.getCase(origin[0] + x, origin[1] + y).getCouleur() != pionSelected.getCouleur():

										listPossibleMove.append((origin[0] + x, origin[1] + y))

								else:

									listPossibleMove.append((origin[0] + x, origin[1] + y))

						if 0 < origin[1] + my < 9:

							if "empty" in self.getCase(origin[0] + x, origin[1] + my).getName():

								listPossibleMove.append((origin[0] + x, origin[1] + my))

							else:

								if not takeFriends:

									if self.getCase(origin[0] + x, origin[1] + my).getCouleur() != pionSelected.getCouleur():

										listPossibleMove.append((origin[0] + x, origin[1] + my))
								else:

									listPossibleMove.append((origin[0] + x, origin[1] + my))

				else:

					y, my = 1, -1

					if 0 < origin[0] + x < 9:

						if 0 < origin[1] + y < 9:

							if "empty" in self.getCase(origin[0] + x, origin[1] + y).getName():

								listPossibleMove.append((origin[0] + x, origin[1] + y))

							else:

								if not takeFriends:

									if self.getCase(origin[0] + x, origin[1] + y).getCouleur() != pionSelected.getCouleur():

										listPossibleMove.append((origin[0] + x, origin[1] + y))

								else:

									listPossibleMove.append((origin[0] + x, origin[1] + y))

						if 0 < origin[1] + my < 9:

							if "empty" in self.getCase(origin[0] + x, origin[1] + my).getName():

								listPossibleMove.append((origin[0] + x, origin[1] + my))

							else:

								if not takeFriends:

									if self.getCase(origin[0] + x, origin[1] + my).getCouleur() != pionSelected.getCouleur():

										listPossibleMove.append((origin[0] + x, origin[1] + my))

								else:

									listPossibleMove.append((origin[0] + x, origin[1] + my))

		# ==============================================================================================================
		# FOU
		# ==============================================================================================================

		elif pionSelected.getType() == "fou":

			upLeft = True
			downLeft = True
			upRight = True
			downRight = True

			for x in range(1, 8):

				if 0 < origin[0] + x < 9 and 0 < origin[1] + x < 9 and downRight:

					if "empty" in self.getCase(origin[0] + x, origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] + x))

					elif "empty" in self.getCase(origin[0] + x, origin[1] + x).getName() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] + x, origin[1] + x))
								downRight = False

							else:

								downRight = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1] + x))

				if 0 < origin[0] - x < 9 and 0 < origin[1] - x < 9 and upLeft:

					if "empty" in self.getCase(origin[0] - x, origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] - x))

					elif "empty" in self.getCase(origin[0] - x, origin[1] - x).getName() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] - x))
					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1] - x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1] - x))
								upLeft = False

							else:

								upLeft = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1] - x))

				if 0 < origin[0] + x < 9 and 0 < origin[1] - x < 9 and upRight:

					if "empty" in self.getCase(origin[0] + x, origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] - x))

					elif "empty" in self.getCase(origin[0] + x, origin[1] - x).getName() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] - x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1] - x).getCouleur() != pionSelected.getCouleur() and upRight:

								listPossibleMove.append((origin[0] + x, origin[1] - x))
								upRight = False

							else:

								upRight = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1] - x))

				if 0 < origin[0] - x < 9 and 0 < origin[1] + x < 9 and downLeft:

					if "empty" in self.getCase(origin[0] - x, origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] + x))

					elif "empty" in self.getCase(origin[0] - x, origin[1] + x).getName() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1] + x))
								downLeft = False

							else:

								downLeft = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1] + x))

		# ==============================================================================================================
		# REINE
		# ==============================================================================================================

		elif pionSelected.getType() == "reine":

			left = True
			right = True

			up = True
			upLeft = True
			upRight = True

			down = True
			downLeft = True
			downRight = True

			for x in range(1, 8):

				# Down Rign --------------------------------------------------------------------------------------------

				if 0 < origin[0] + x < 9 and 0 < origin[1] + x < 9 and downRight:

					if "empty" in self.getCase(origin[0] + x, origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] + x))

					elif self.getCase(origin[0] + x, origin[1] + x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] + x, origin[1] + x))
								downRight = False

							else:

								downRight = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1] + x))

				# Up Left ----------------------------------------------------------------------------------------------

				if 0 < origin[0] - x < 9 and 0 < origin[1] - x < 9 and upLeft:

					if "empty" in self.getCase(origin[0] - x, origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] - x))

					elif self.getCase(origin[0] - x, origin[1] - x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] - x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1] - x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1] - x))
								upLeft = False

							else:

								upLeft = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1] - x))

				# Up Right ---------------------------------------------------------------------------------------------

				if 0 < origin[0] + x < 9 and 0 < origin[1] - x < 9 and upRight:

					if "empty" in self.getCase(origin[0] + x, origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] - x))

					elif self.getCase(origin[0] + x, origin[1] - x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1] - x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1] - x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] + x, origin[1] - x))
								upRight = False

							else:

								upRight = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1] - x))

				# Down Left --------------------------------------------------------------------------------------------

				if 0 < origin[0] - x < 9 and 0 < origin[1] + x < 9 and downLeft:

					if "empty" in self.getCase(origin[0] - x, origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] + x))

					elif self.getCase(origin[0] - x, origin[1] + x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1] + x))
								downLeft = False

							else:

								downLeft = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1] + x))

				# Up ---------------------------------------------------------------------------------------------------

				if 0 < origin[1] + x < 9 and up:

					if "empty" in self.getCase(origin[0], origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0], origin[1] + x))

					elif self.getCase(origin[0], origin[1] + x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0], origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0], origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0], origin[1] + x))
								up = False

							else:

								up = False

						else:

							listPossibleMove.append((origin[0], origin[1] + x))

				# Down -------------------------------------------------------------------------------------------------

				if 0 < origin[1] - x < 9 and down:

					if "empty" in self.getCase(origin[0], origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0], origin[1] - x))

					elif self.getCase(origin[0], origin[1] - x).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0], origin[1] - x))

					else:

						if not takeFriends:

							if self.getCase(origin[0], origin[1] - x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0], origin[1] - x))
								down = False

							else:

								down = False

						else:

							listPossibleMove.append((origin[0], origin[1] - x))

				# Left -------------------------------------------------------------------------------------------------

				if 0 < origin[0] - x < 9 and left:

					if "empty" in self.getCase(origin[0] - x, origin[1]).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1]))

					elif self.getCase(origin[0] - x, origin[1]).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1]))

					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1]).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1]))
								left = False

							else:

								left = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1]))

				# Right ------------------------------------------------------------------------------------------------

				if 0 < origin[0] + x < 9 and right:

					if "empty" in self.getCase(origin[0] + x, origin[1]).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1]))

					elif self.getCase(origin[0] + x, origin[1]).getCouleur() != pionSelected.getCouleur() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1]))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1]).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] + x, origin[1]))
								right = False

							else:

								right = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1]))

		# ==============================================================================================================
		# ROI
		# ==============================================================================================================

		elif pionSelected.getType() == "roi":

			left = True
			right = True

			up = True
			upLeft = True
			upRight = True

			down = True
			downLeft = True
			downRight = True

			x = 1

			# Down Rign --------------------------------------------------------------------------------------------

			if 0 < origin[0] + x < 9 and 0 < origin[1] + x < 9 and downRight:

				if "empty" in self.getCase(origin[0] + x, origin[1] + x).getName():

					listPossibleMove.append((origin[0] + x, origin[1] + x))

				else:

					if not takeFriends:

						if self.getCase(origin[0] + x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] + x, origin[1] + x))
							downRight = False

						else:

							downRight = False

					else:

						listPossibleMove.append((origin[0] + x, origin[1] + x))

			# Up Left ----------------------------------------------------------------------------------------------

			if 0 < origin[0] - x < 9 and 0 < origin[1] - x < 9 and upLeft:

				if "empty" in self.getCase(origin[0] - x, origin[1] - x).getName():

					listPossibleMove.append((origin[0] - x, origin[1] - x))

				else:

					if not takeFriends:

						if self.getCase(origin[0] - x, origin[1] - x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] - x, origin[1] - x))
							upLeft = False

						else:

							upLeft = False

					else:

						listPossibleMove.append((origin[0] - x, origin[1] - x))

			# Up Right ---------------------------------------------------------------------------------------------

			if 0 < origin[0] + x < 9 and 0 < origin[1] - x < 9 and upRight:

				if "empty" in self.getCase(origin[0] + x, origin[1] - x).getName():

					listPossibleMove.append((origin[0] + x, origin[1] - x))

				else:

					if not takeFriends:

						if self.getCase(origin[0] + x, origin[1] - x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] + x, origin[1] - x))
							upRight = False

						else:

							upRight = False

					else:

						listPossibleMove.append((origin[0] + x, origin[1] - x))

			# Down Left --------------------------------------------------------------------------------------------

			if 0 < origin[0] - x < 9 and 0 < origin[1] + x < 9 and downLeft:

				if "empty" in self.getCase(origin[0] - x, origin[1] + x).getName():

					listPossibleMove.append((origin[0] - x, origin[1] + x))

				else:

					if not takeFriends:

						if self.getCase(origin[0] - x, origin[1] + x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] - x, origin[1] + x))
							downLeft = False

						else:

							downLeft = False

					else:

						listPossibleMove.append((origin[0] - x, origin[1] + x))

			# Up ---------------------------------------------------------------------------------------------------

			if 0 < origin[1] + x < 9 and up:

				if "empty" in self.getCase(origin[0], origin[1] + x).getName():

					listPossibleMove.append((origin[0], origin[1] + x))

				else:

					if not takeFriends:

						if self.getCase(origin[0], origin[1] + x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0], origin[1] + x))
							up = False

						else:

							up = False

					else:

						listPossibleMove.append((origin[0], origin[1] + x))

			# Down -------------------------------------------------------------------------------------------------

			if 0 < origin[1] - x < 9 and down:

				if "empty" in self.getCase(origin[0], origin[1] - x).getName():

					listPossibleMove.append((origin[0], origin[1] - x))

				else:

					if not takeFriends:

						if self.getCase(origin[0], origin[1] - x).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0], origin[1] - x))
							down = False

						else:

							down = False

					else:

						listPossibleMove.append((origin[0], origin[1] - x))

			# Left -------------------------------------------------------------------------------------------------

			if 0 < origin[0] - x < 9 and left:

				if "empty" in self.getCase(origin[0] - x, origin[1]).getName():

					listPossibleMove.append((origin[0] - x, origin[1]))

				else:

					if not takeFriends:

						if self.getCase(origin[0] - x, origin[1]).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] - x, origin[1]))
							left = False

						else:

							left = False

					else:

						listPossibleMove.append((origin[0] - x, origin[1]))

			# Right ------------------------------------------------------------------------------------------------

			if 0 < origin[0] + x < 9 and right:

				if "empty" in self.getCase(origin[0] + x, origin[1]).getName():

					listPossibleMove.append((origin[0] + x, origin[1]))

				else:

					if not takeFriends:

						if self.getCase(origin[0] + x, origin[1]).getCouleur() != pionSelected.getCouleur():

							listPossibleMove.append((origin[0] + x, origin[1]))
							right = False

						else:

							right = False

					else:

						listPossibleMove.append((origin[0] + x, origin[1]))

		# ==============================================================================================================
		# TOUR
		# ==============================================================================================================

		elif pionSelected.getType() == "tour":

			left = True
			right = True
			up = True
			down = True

			for x in range(1, 8):

				# Up ---------------------------------------------------------------------------------------------------

				if 0 < origin[1] + x < 9 and up:

					if "empty" in self.getCase(origin[0], origin[1] + x).getName() and not goThrough:

						listPossibleMove.append((origin[0], origin[1] + x))

					elif "empty" in self.getCase(origin[0], origin[1] + x).getName() and goThrough:

						listPossibleMove.append((origin[0], origin[1] + x))

					else:

						if not takeFriends:

							if self.getCase(origin[0], origin[1] + x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0], origin[1] + x))
								up = False

							else:

								up = False

						else:

							listPossibleMove.append((origin[0], origin[1] + x))

				# Down -------------------------------------------------------------------------------------------------

				if 0 < origin[1] - x < 9 and down:

					if "empty" in self.getCase(origin[0], origin[1] - x).getName() and not goThrough:

						listPossibleMove.append((origin[0], origin[1] - x))

					elif "empty" in self.getCase(origin[0], origin[1] - x).getName() and goThrough:

						listPossibleMove.append((origin[0], origin[1] - x))

					else:

						if not takeFriends:

							if self.getCase(origin[0], origin[1] - x).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0], origin[1] - x))
								down = False

							else:

								down = False

						else:

							listPossibleMove.append((origin[0], origin[1] - x))

				# Left -------------------------------------------------------------------------------------------------

				if 0 < origin[0] - x < 9 and left:

					if "empty" in self.getCase(origin[0] - x, origin[1]).getName() and not goThrough:

						listPossibleMove.append((origin[0] - x, origin[1]))

					elif "empty" in self.getCase(origin[0] - x, origin[1]).getName() and goThrough:

						listPossibleMove.append((origin[0] - x, origin[1]))

					else:

						if not takeFriends:

							if self.getCase(origin[0] - x, origin[1]).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] - x, origin[1]))
								left = False

							else:

								left = False

						else:

							listPossibleMove.append((origin[0] - x, origin[1]))

				# Right ------------------------------------------------------------------------------------------------

				if 0 < origin[0] + x < 9 and right:

					if "empty" in self.getCase(origin[0] + x, origin[1]).getName() and not goThrough:

						listPossibleMove.append((origin[0] + x, origin[1]))

					elif "empty" in self.getCase(origin[0] + x, origin[1]).getName() and goThrough:

						listPossibleMove.append((origin[0] + x, origin[1]))

					else:

						if not takeFriends:

							if self.getCase(origin[0] + x, origin[1]).getCouleur() != pionSelected.getCouleur():

								listPossibleMove.append((origin[0] + x, origin[1]))
								right = False

							else:

								right = False

						else:

							listPossibleMove.append((origin[0] + x, origin[1]))

		return listPossibleMove
