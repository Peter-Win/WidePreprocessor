from Taxon import Taxon
class TaxonCast(Taxon):
	""" Специальный метод класса, выполняющий преобразования типа """
	type = 'Cast'

	def getLocalType(self):
		return self.items[0]

	def getBody(self):
		return self.items[1]

	def getSimpleName(self):
		localType = self.getLocalType()
		if localType.type == 'TypeName':
			return localType.getTypeTaxon().name