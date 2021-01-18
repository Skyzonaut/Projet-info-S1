
class pion:
	"""
	Constructeur de la classe pion, représentant un pion d'échec avec toutes ses caractéristiques jouables.
	Et les informations permettant de le faire évoluter dans un plateau et un jeu.
	"""

	def __init__(self, _name: str, _type: str, _couleur: str, _state: bool, _image):
		"""
		Constructeur de la classe pion, représentant un pion d'échec avec toutes ses caractéristiques jouables.
		Et les informations permettant de le faire évoluter dans un plateau et un jeu.

		:param _name: nom du pion, contenant son numéro (pour les pions qui peuvent avoir le même type), sa couleur et
			son type
		:param _type: le type du pion : Tour, cavalier, fou, roi, reine, pion
		:param _couleur: sa couleur : Blanc ou Noir
		:param _state: état du pion représentant son état dans le jeu : False = Mort, True = Encore sur le plateau
		:param _image: image du pion. Chaque pion possède l'image qu'il doit afficher sur le plateau pour pouvoir y
			accéder plus rapidement et plus facilement
		"""
		self.name = _name
		self.type = _type
		self.couleur = _couleur
		self.state = _state
		self.image = _image

	#Getter
	def getName(self): return self.name;
	def getType(self): return self.type;
	def getCouleur(self): return self.couleur;
	def getState(self): return self.state;
	def getImage(self): return self.image;

	#Setter
	def setName(self, newName): self.name = newName
	def setType(self, newType): self.type = newType
	def setCouleur(self, newCouleur): self.couleur = newCouleur
	def setState(self, newState): self.state = newState
	def setImage(self, newImage): self.image = newImage

	def apercu(self):
		"""
		Print sur le terminal un récapitulatif du pion et de ses caractéristiques
		"""

		print(f'Name: {self.name}')
		print(f'Type: {self.type}')
		print(f'Couleur: {self.couleur}')
		print(f'State: {self.state}')
		print(f'Image: {self.image}')

	def getApercu(self):
		"""
		Retourne une chaîne de caractères comprenant un récapitulatif du pion et de ses caractéristiques
		"""

		final_string = ""
		final_string += (f'Name: {self.name}\n')
		final_string += (f'Type: {self.type}\n')
		final_string += (f'Couleur: {self.couleur}\n')
		final_string += (f'State: {self.state}\n')
		final_string += (f'Image: {self.image}\n')
		final_string += ("\n")

		return final_string