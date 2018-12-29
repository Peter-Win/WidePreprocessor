from Taxon import Taxon
class TaxonDictionary(Taxon):
	def __init__(self):
		super().__init__()
		self.dictionary = {}

	def addNamedItem(self, item):
		self.dictionary[item.name] = item
		return self.addItem(item)

	def findUp(self, name, fromWho, source):
		""" Поиск с подъёмом вверх.
		Большинство таксонов могут лишь проверить себя и вызвать поиск владельца
		"""
		if self.name == name:
			return self
		# Поиск среди элементов словаря
		item = self.dictionary.get(name)
		if item:
			return item
		if self.owner:
			return self.owner.findUp(name, self, source)

	def clone(self, newCore):
		newTaxon = super().clone(newCore)
		for i, item in enumerate(self.items):
			if item.name in self.dictionary:
				newTaxon.dictionary[item.name] = newTaxon.items[i]
		return newTaxon
