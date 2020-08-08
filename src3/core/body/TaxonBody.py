from Taxon import Taxon

class TaxonBody(Taxon):
	type = 'body'

	def isEmpty(self):
		for taxon in self.items:
			if taxon.type != 'comment':
				return False
		return True