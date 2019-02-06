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
	def matchQuasi(self, quasiType):
		return self.getTypeTaxon().matchQuasi(quasiType)

class TaxonTypePath(TaxonTypeName):
	type = 'TypePath'
	def __init__(self, path = ''):
		super().__init__()
		self.path = path
		self.taxPath = None
	def clone(self, newCore):
		result = super().clone(newCore)
		result.path = self.path
		return result

	def getTypeTaxon(self):
		return self.taxPath[-1]
	def onUpdate(self):
		if not self.taxPath:
			chunks = self.path.split('.')
			self.taxPath = [self.findUpEx(chunks[0])]
			for word in chunks[1:]:
				taxon = self.taxPath[-1].dictionary.get(word)
				if not taxon:
					self.throwError('Invalid field "'+word+'" in '+self.path)
				self.taxPath.append(taxon)



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