
class event:
	"""
	Classe d'objet permettant de stocker des informations lors d'un clic
	et qui seront accessible lors des clics suivants
	"""
	def __init__(self, _id: int,
				 _origin: tuple,
				 _action: str,
				 _cache=None,
				 _trace=None,
				 _echecTrace=None,
				 _sauveteur=None,
				 _enableButton=None):
		"""
		:param _id: Identifiant de l'évènements
		:param _origin: Case (tuple) qui a été cliquée et sur laquelle porte l'évènement
		:param _action: Type de clic : "clic" = Sélection du pion | "Place" = Sélection de la case où le déplacer
		:param _cache: Sert à stocker l'image du pion précédemment sélectionné
		:param _trace: Sert à stocker les déplacements possibles du pion précédemment sélectionné
		:param _echecTrace: Sert à stocker les pions mettant en échec les rois
		:param _sauveteur: Sert à stocker les pions pouvant sauver d'un echec son roi
		:param _enableButton: Sert à stocker les boutons/case à désactiver et réactiver lors d'un echec
		"""
		self.id = _id
		self.origin = _origin
		self.action = _action
		self.cache = _cache
		self.trace = _trace
		self.echecTrace = _echecTrace
		self.sauveteur = _sauveteur
		self.enabledButton = _enableButton

	# Getter
	# Sert à récupérer les caractéristiques de l'évènement
	def getId(self): return self.id
	def getOrigin(self): return self.origin
	def getAction(self): return self.action
	def getCache(self): return self.cache
	def getTrace(self): return self.trace
	def getEchecTrace(self): return self.echecTrace
	def getSauveteur(self): return self.sauveteur
	def getEnabledButton(self): return self.enabledButton

	# Setter
	# Sert à modifier les caractéristiques de l'évènement
	def setId(self, newId): self.id = newId
	def setOrigin(self, newOrigins): self.origin = newOrigins
	def setAction(self, newAction): self.action = newAction
	def setCache(self,  newCache): self.cache = newCache
	def setTrace(self, newTrace): self.trace = newTrace
	def setEchecTrace(self, newEchecTrace): self.echecTrace = newEchecTrace
	def setSauveteur(self, newSauveteur): self.sauveteur = newSauveteur
	def setEnabledButton(self, newEnabledButton): self.enabledButton = newEnabledButton

	# DEBUG
	# Sert à afficher les informations de l'évènement sur le Terminal
	def apercu(self):
		print("@ " + "-" * 30)
		print("| Id     : " + str(self.id))
		print("| Origin : " + str(self.origin))
		print("| Action : " + str(self.action))
		print("| Cache  : " + str(self.cache))
		print("| Trace  : " + str(self.trace))
		print("| Echec  : " + str(self.echecTrace))
		print("| Saver  : " + str(self.sauveteur))
		print("| BtnOn  : " + str(self.enabledButton))

