from Taxon import Taxon

class TaxonType(Taxon):
	""" Абстрактный класс типа """
	type = 'Type'

class TaxonTypeName(TaxonType):
	""" Тип со ссылкой на объект по имени. Может быть класс, встроенный тип, enum, typedef """
	type = 'TypeName'
	def getTypeTaxon(self):
		return self.refs['type']
	def getDefaultValue(self):
		return self.getTypeTaxon().getDefaultValue()

class TaxonTypeArray(TaxonType):
	type = 'TypeArray'
	def getItemType(self):
		return self.items[0]