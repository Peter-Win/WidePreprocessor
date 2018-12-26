from Taxon import Taxon
class TaxonDictionary(Taxon):
	def __init__(self):
		super().__init__()
		self.dictionary = {}

	def addNamedItem(self, item):
		self.dictionary[item.name] = item
		return self.addItem(item)

	def clone(self, newCore):
		newTaxon = super().clone(newCore)
		for i, item in enumerate(self.items):
			if item.name in self.dictionary:
				newTaxon.dictionary[item.name] = newTaxon.items[i]
		return newTaxon
