from core.TaxonScalar import TaxonScalar

class TSScalar(TaxonScalar):
	def getName(self):
		if self.name == 'bool':
			return 'boolean'
		return 'number'