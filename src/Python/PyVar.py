from core.TaxonVar import TaxonVar, TaxonField, TaxonParam
from Python.PyTaxon import PyTaxon

class PyCommonVar(PyTaxon):		
	def export(self, outContext):
		expr = self.getValueTaxon()
		if expr:
			val = expr.exportString()
		else:
			val = 'None'	# TODO: Значение по умолчанию для используемого типа
		outContext.writeln(self.getName(self) + ' = ' + val)

class PyVar(TaxonVar, PyCommonVar):
	def getName(self, user):
		if self.owner.type != 'Module':
			return self.name
		return super().getName(user)

class PyField(TaxonField, PyCommonVar):
	def export(self, outContext):
		if 'static' not in self.attrs:
			return
		super().export(outContext)

class PyParam(TaxonParam, PyCommonVar):
	def getName(self, user):
		return self.name

	def exportString(self):
		s = self.getName(self)
		expr = self.getValueTaxon()
		if expr:
			s += ' ' + expr.exportString()
		return s
