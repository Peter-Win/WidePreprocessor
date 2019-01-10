from core.TaxonModule import TaxonModule
from Taxon import Taxon

class PyCore(TaxonModule):
	def __init__(self):
		super().__init__()
		self.name = 'Python'
		self.core = self
		from Python.core.PyTaxonMap import PyTaxonMap
		from Python.core.PyCoreFunctions import initFunctions
		self.taxonMap = PyTaxonMap

		# Scalar types
		for name, value in Scalars:
			self.addNamedItem(PyTypeScalar(name, value))

		from Python.core.PyString import PyString
		self.addNamedItem(PyString())

		initFunctions(self)

Scalars = [
	('int', '0'),
	('long', '0'),
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
