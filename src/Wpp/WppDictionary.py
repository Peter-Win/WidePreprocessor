from Wpp.WppTaxon import WppTaxon
class WppDictionary(WppTaxon):
	def addTaxon(self, taxon):
		return self.addNamedItem(taxon)