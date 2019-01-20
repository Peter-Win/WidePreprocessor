from Taxon import Taxon

class TaxonTypedef(Taxon):
	type = 'Typedef'
	def getTypeTaxon(self):
		return self.items[0]