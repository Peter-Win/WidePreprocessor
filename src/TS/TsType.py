from core.TaxonType import TaxonTypeName, TaxonTypeArray, TaxonTypeMap, TaxonTypePath

class TsTypeName(TaxonTypeName):
	def exportString(self):
		return self.getTypeTaxon().getName(self)

class TsTypePath(TaxonTypePath):
	def exportString(self):
		names = [taxon.getName(self) for taxon in self.taxPath]
		return '.'.join(names)

class TsTypeArray(TaxonTypeArray):
	def exportString(self):
		return self.getItemType().exportString() + '[]'

class TsTypeMap(TaxonTypeMap):
	def exportString(self):
		return 'Map<%s, %s>' % (self.getKeyType().exportString(), self.getValueType().exportString())
