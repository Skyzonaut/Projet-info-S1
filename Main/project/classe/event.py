
class event:

	def __init__(self, _id, _origin, _action, _destination=None):
		self.id = _id
		self.origin = _origin
		self.action = _action
		self.destination = _destination

	def getId(self): return self.id
	def getOrigin(self): return self.origin
	def getAction(self): return self.action
	def getDestination(self): return self.destination

	def setId(self, newId): self.id = newId
	def setOrigin(self, newOrigins): self.origin = newOrigins
	def setAction(self, newAction): self.action = newAction
	def setDestination(self,  newDestination): self.destination = newDestination

	def apercu(self):
		print("|" + "-" * 20)
		print("| Id          : " + str(self.id))
		print("| Origin      : " + str(self.origin))
		print("| Action      : " + str(self.action))
		print("| Destination : " + str(self.destination))

