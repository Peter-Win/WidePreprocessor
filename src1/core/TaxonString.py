from TaxonDictionary import TaxonDictionary

class TaxonString(TaxonDictionary):
	type = 'String'
	__slots__ = ()

	def isType(self):
		return True

	def buildQuasiType(self):
		qt = super().buildQuasiType()
		qt.itemType = self	# Это нужно для доступа через индекс value[i]
		return qt

	def matchQuasiType(self, left, right):
		if right.type == 'Const' and right.taxon.constType == 'string':
			return 'constExact', None
		if right.type == 'String':
			return 'exact', None
		return None, None