from core.TaxonModule import TaxonModule
from Taxon import Taxon

class TsCore(TaxonModule):
	def __init__(self):
		super().__init__()
		self.name = 'TypeScript'
		self.core = self
		from TS.core.TsTaxonMap import TsTaxonMap
		from TS.core.TsString import TsString

		self.taxonMap = TsTaxonMap
		self.addNamedItem(TsString())

		Scalars = [
			('bool', 'boolean', 'False'),
			('int', 'number', '0'),
			('long', 'number', '0'),
			('float', 'number', '0.0'),
			('double', 'number', '0.0')
		]
		for name, exportName, defaultValue in Scalars:
			self.addNamedItem(TsScalar(name, exportName, defaultValue))

class TsScalar(Taxon):
	type = 'TypeScalar'
	def __init__(self, name, exportName, defaultValue):
		super().__init__()
		self.name = name
		self.exportName = exportName
		self.defaultValue = defaultValue

	def getName(self, user):
		return self.exportName

	def getDefaultValue(self):
		if self.name == 'bool':
			return self.core.taxonMap[self.defaultValue]()
		return self.core.taxonMap['Const'](self.name, self.defaultValue)

	def exportString(self):
		return self.name

