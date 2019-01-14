from core.TaxonType import TaxonTypeName, TaxonTypeArray

class PyTypeName(TaxonTypeName):
	pass

class PyTypeArray(TaxonTypeArray):
	def exportCollection(self, user, bUseIndex):
		s = user.exportString()
		if bUseIndex:
			s = 'enumerate('+s+')'
		return s