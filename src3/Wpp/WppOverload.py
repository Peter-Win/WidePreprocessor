from core.TaxonOverload import TaxonOverload

class WppOverload(TaxonOverload):
	def readBody(self, context):
		return self.items[-1].readBody(context)

	def addTaxon(self, taxon, context):
		return self.items[-1].addTaxon(taxon, context)

	def export(self, outContext):
		for item in self.items:
			item.export(outContext)