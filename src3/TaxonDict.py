from Taxon import Taxon

class TaxonDict(Taxon):
	__slots__ = ('dict')
	def __init__(self, name=''):
		super().__init__(name)
		self.dict = {}

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.dict = src.dict.copy()

	def addItem(self, item):
		if item.name:
			self.dict[item.name] = item
		return super().addItem(item)

	def findItem(self, name):
		return self.dict.get(name)

	def removeItem(self, item):
		if item.name:
			del self.dict[item.name]
		super().removeItem(item)