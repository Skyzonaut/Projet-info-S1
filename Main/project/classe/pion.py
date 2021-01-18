
class pion:

	def __init__(self, _name: str, _type: str, _couleur: str, _state: bool, _image) -> None:

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
		print(f'Name: {self.name}')
		print(f'Type: {self.type}')
		print(f'Couleur: {self.couleur}')
		print(f'State: {self.state}')
		print(f'Image: {self.image}')

	def getApercu(self):
		final_string = ""
		final_string += (f'Name: {self.name}\n')
		final_string += (f'Type: {self.type}\n')
		final_string += (f'Couleur: {self.couleur}\n')
		final_string += (f'State: {self.state}\n')
		final_string += (f'Image: {self.image}\n')
		final_string += ("\n")

		return final_string