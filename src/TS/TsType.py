from core.TaxonType import TaxonTypeName, TaxonTypeArray, TaxonTypeMap, TaxonTypePath

class TsType:
	def defaultReplaceMode(self):
		return 'extern'

	def exportString(self):
		decl = self.getDecl()
		if hasattr(decl, 'exportUsage'):
			return decl.exportUsage()
		return self._exportString()

class TsTypeName(TaxonTypeName, TsType):
	def defaultReplaceMode(self):
		return 'replace'
	def getDecl(self):
		return self.getTypeTaxon()
	def _exportString(self):
		return self.getTypeTaxon().getName(self)

class TsTypePath(TaxonTypePath, TsType):
	def defaultReplaceMode(self):
		return 'replace'
	def getDecl(self):
		return self.getTypeTaxon()
	def _exportString(self):
		names = [taxon.getName(self) for taxon in self.taxPath]
		return '.'.join(names)+'!'

class TsTypeArray(TaxonTypeArray, TsType):
	def getDecl(self):
		return self.core.dictionary['Array']
	def _exportString(self):
		return self.getItemType().exportString() + '[]'

class TsTypeMap(TaxonTypeMap, TsType):
	def getDecl(self):
		return self.core.dictionary['Map']
	def _exportString(self):
		return 'Map<%s, %s>' % (self.getKeyType().exportString(), self.getValueType().exportString())
