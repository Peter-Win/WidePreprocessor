from TaxonDict import TaxonDict

class TaxonModule(TaxonDict):
	type = 'module'

	def isModule(self):
		return True