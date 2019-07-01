from Taxon import Taxon

class TaxonTypedef(Taxon):
	"""
	typedef здесь может быть в составе модуля, в составе класса или в блоке
	Единственный подчиненный элемент - локальный тип
	"""
	type = 'Typedef'
	__slots__ = ()
	def isType(self):
		return True
	def getLocalType(self):
		return self.items[0]
	def isReady(self):
		return self.getLocalType().isReady()
	def isReadyFull(self):
		return self.getLocalType().isReadyFull()
	def buildQuasiType(self):
		return self.getLocalType().buildQuasiType()
