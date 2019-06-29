class Ref:
	def __init__(self, name, target = None):
		self.name = name
		self.target = target

	def setTarget(self, target):
		self.target = target

	def isReady(self):
		return self.target != None

	def isReadyFull(self):
		return self.isReady() and self.target.isReadyFull()

	def clone(self):
		return Ref(self.name)

	def find(self, taxon):
		self.target = taxon.findUpPath(self.name)

	def getDebugStr(self):
		return '%s=>%s' % (self.name, '%s:%s' % (self.target.type, self.target.getDebugStr()) if self.target else 'None')