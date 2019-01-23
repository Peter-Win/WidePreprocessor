from core.TaxonCast import TaxonCast
from Python.PyTaxon import PyTaxon

class PyCast(TaxonCast):
	def export(self, outContext):
		typeName = self.getSimpleName()
		methodName = ''
		if typeName == 'String':
			methodName = '__str__'
		if methodName:
			s = 'def '+methodName+'(self):'
			outContext.writeln(s)
			self.getBody().export(outContext)
