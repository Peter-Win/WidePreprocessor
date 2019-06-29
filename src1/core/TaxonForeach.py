from Taxon import Taxon

class TaxonForeach(Taxon):
	""" for index, value in collection {body}"""
	type = 'Foreach'
	__slots__ = ('value', 'index')
	refsList = ('value', 'index')
	def __init__(self):
		super().__init__()
		self.value = None
		self.index = None

	def getBody(self):
		return self.items[0]
	def getCollection(self):
		return self.items[1]
	def getValue(self):
		if self.isValueLocal():
			return self.items[2]
		return self.value and self.value.target
	def isValueLocal(self):
		return 'localValue' in self.attrs
	def getIndex(self):
		if self.isIndexLocal():
			n = 3 if self.isValueLocal() else 2
			return self.items[n]
		return self.index and self.index.target
	def isIndexLocal(self):
		return 'localIndex' in self.attrs