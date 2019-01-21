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
		from Python.core.PyArray import PyArray
		from Python.core.PyMath import PyMath
		self.addNamedItem(PyString())
		self.addNamedItem(PyArray())
		self.addNamedItem(PyMath())

		initFunctions(self)

Scalars = [
	('bool', 'False'),
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
		if self.name == 'bool':
			return self.core.taxonMap[self.defaultValue]()
		return self.core.taxonMap['Const'](self.name, self.defaultValue)
