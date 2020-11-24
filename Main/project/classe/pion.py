
class pion:

	def __init__(self, _name, _type, _couleur, _state, _image):

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
	def setType(self, newType): self.name = newType
	def setCouleur(self, newCouleur): self.name = newCouleur
	def setState(self, newState): self.name = newState
	def setNImage(self, newImage): self.name = newImage

	def apercu(self):
		print(f'Name: {self.name}')
		print(f'Type: {self.type}')
		print(f'Couleur: {self.couleur}')
		print(f'State: {self.state}')
		print(f'Image: {self.image}')