
class event:

	def __init__(self, _id, _origin, _action, _cache=None):
		self.id = _id
		self.origin = _origin
		self.action = _action
		self.cache = _cache

	def getId(self): return self.id
	def getOrigin(self): return self.origin
	def getAction(self): return self.action
	def getCache(self): return self.cache

	def setId(self, newId): self.id = newId
	def setOrigin(self, newOrigins): self.origin = newOrigins
	def setAction(self, newAction): self.action = newAction
	def setCache(self,  newCache): self.cache = newCache

	def apercu(self):
		print("@" + "-" * 30)
		print("| Id     : " + str(self.id))
		print("| Origin : " + str(self.origin))
		print("| Action : " + str(self.action))
		print("| Cache  : " + str(self.cache))

