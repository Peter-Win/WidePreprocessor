from core.TaxonModule import TaxonModule
from Taxon import Taxon

class PyCore(TaxonModule):
	def __init__(self):
		super().__init__()
		self.name = 'Python'
		self.core = self
		from Python.core.PyTaxonMap import PyTaxonMap
		self.taxonMap = PyTaxonMap

		# Scalar types
		for name, value in Scalars:
			self.addNamedItem(PyTypeScalar(name, value))


Scalars = [
	('int', '0'),
	('float', '0.0'),
	('double', '0.0')
]
class PyTypeScalar(Taxon):
	type = 'TypeScalar'
	def __init__(self, name, defaultValue):
		super().__init__()
		self.name = name
		self.defaultValue = defaultValue

	def getDefaultValue(self):
		return self.core.taxonMap['Const'](self.name, self.defaultValue)
