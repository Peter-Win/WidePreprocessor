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
	def getFieldDeclaration(self, name):
		return self.getTypeTaxon().getFieldDeclaration(name)

class TaxonTypeArray(TaxonType):
	type = 'TypeArray'
	def getItemType(self):
		return self.items[0]
	def getArray(self):
		return self.core.dictionary['Array']
	def getFieldDeclaration(self, name):
		return self.getArray().getFieldDeclaration(name)
	def getDefaultValue(self):
		return self.getArray().getDefaultValue()

class TaxonTypeMap(TaxonType):
	type = 'TypeMap'
	def getKeyType(self):
		return self.items[0]
	def getValueType(self):
		return self.items[1]