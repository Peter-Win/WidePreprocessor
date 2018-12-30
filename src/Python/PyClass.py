from core.TaxonClass import TaxonClass
from Python.PyTaxon import PyTaxon

class PyClass(TaxonClass, PyTaxon):
	def export(self, outContext):
		s = 'class ' + self.getName(self)
		parent = self.getParent()
		if parent:
			s += '(' + parent.getName(self) + ')'
		s += ':'
		outContext.writeln(s)
		outContext.level += 1
		outContext.writeln('pass')
		outContext.level -= 1