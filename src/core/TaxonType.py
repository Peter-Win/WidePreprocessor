from Taxon import Taxon

class TaxonType(Taxon):
	""" Абстрактный класс типа """
	type = 'Type'

class TaxonTypeName(TaxonType):
	""" Тип со ссылкой на объект по имени. Может быть класс, встроенный тип, enum, typedef """
	type = 'TypeName'
	def getTypeTaxon(self):
		return self.refs['type']