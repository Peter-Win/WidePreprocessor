from Taxon import Taxon

class TaxonDictionary(Taxon):
	__slots__ = ('dictionary',)
	excludes = ('dictionary',)
	
	def __init__(self, name = ''):
		super().__init__(name)
		self.dictionary = {}

	def addNamedItem(self, item):
		self.dictionary[item.name] = item
		return self.addItem(item)

	def findUp(self, fromWho, params):
		""" Поиск с подъёмом вверх.
		"""
		if self.isMatch(params):
			return self
		# Поиск среди элементов словаря
		item = self.dictionary.get(params['name'])
		if item and item.isMatch(params):
			return item
		if self.owner:
			return self.owner.findUp(self, params)

	def _clone(self, newCore):
		newTaxon = super()._clone(newCore)
		for i, item in enumerate(self.items):
			if item.name in self.dictionary:
				newTaxon.dictionary[item.name] = newTaxon.items[i]
		return newTaxon
