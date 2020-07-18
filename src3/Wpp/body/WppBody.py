from core.body.TaxonBody import TaxonBody
from Wpp.WppTaxon import WppTaxon

class WppBody(TaxonBody, WppTaxon):
	validSubTaxons = ('if', 'return', 'var')

	def readBody(self, context):
		taxonType = context.getFirstWord()
		lastTaxon = self.items[-1] if len(self.items) > 0 else None
		if taxonType in ('elif', 'else') and lastTaxon and lastTaxon.type == 'if':
			return lastTaxon
		return super().readBody(context)

	def addTaxon(self, taxon):
		if len(self.items) > 0 and self.items[-1] == taxon:
			return taxon
		return super().addTaxon(taxon)

	def export(self, outContext):
		with outContext:
			for tx in self.items:
				tx.export(outContext)

	def findUp(self, name, caller):
		for taxon in self.items:
			if taxon == caller:
				break
			if taxon.name == name:
				return taxon

		return super().findUp(name, caller)
