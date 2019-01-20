from Python.PyTaxon import PyTaxon
from Python.PyClass import PyClass

class PyArray(PyClass):
	def __init__(self):
		super().__init__()
		self.name = 'Array'
		self.addNamedItem(PyArrayPush(name = 'push'))

	def getDefaultValue(self):
		return self.core.taxonMap['ArrayValue']()

class PyArrayPush(PyTaxon):
	type = 'ArrayPush'
	def getName(self, user):
		return 'append'