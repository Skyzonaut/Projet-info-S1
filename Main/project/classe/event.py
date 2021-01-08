
class event:

	def __init__(self, _id, _origin, _action, _cache=None, _trace=None, _echecTrace=None, _sauveteur=None):
		self.id = _id
		self.origin = _origin
		self.action = _action
		self.cache = _cache
		self.trace = _trace
		self.echecTrace = _echecTrace
		self.sauveteur = _sauveteur

	def getId(self): return self.id
	def getOrigin(self): return self.origin
	def getAction(self): return self.action
	def getCache(self): return self.cache
	def getTrace(self): return self.trace
	def getEchecTrace(self): return self.echecTrace
	def getSauveteur(self): return self.sauveteur

	def setId(self, newId): self.id = newId
	def setOrigin(self, newOrigins): self.origin = newOrigins
	def setAction(self, newAction): self.action = newAction
	def setCache(self,  newCache): self.cache = newCache
	def setTrace(self, newTrace): self.trace = newTrace
	def setEchecTrace(self, newEchecTrace): self.echecTrace = newEchecTrace
	def setSauveteur(self, newSauveteur): self.sauveteur = newSauveteur

	def apercu(self):
		print("@ " + "-" * 30)
		print("| Id     : " + str(self.id))
		print("| Origin : " + str(self.origin))
		print("| Action : " + str(self.action))
		print("| Cache  : " + str(self.cache))
		print("| Trace  : " + str(self.trace))
		print("| Echec  : " + str(self.echecTrace))
		print("| Saver  : " + str(self.sauveteur))

