from core.TaxonVar import TaxonVar, TaxonField, TaxonReadonly, TaxonParam
from Python.PyTaxon import PyTaxon

class PyCommonVar(PyTaxon):		
	def export(self, outContext):
		expr = self.getValueTaxon()
		if expr:
			val = expr.exportString()
		else:
			val = self.getLocalType().getDefaultValue().exportString()
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

class PyReadonly(TaxonReadonly, PyCommonVar):
	def getPrivateFieldName(self):
		return '_' + self.getName(self)

	def getName(self, user):
		if user == self.owner or user.type == 'Constructor':
			return self.getPrivateFieldName()
		return super().getName(user)

	def export(self, outContext):
		outContext.writeln('@property')
		outContext.writeln('def ' + self.getName(self) + '(self):')
		outContext.level += 1
		self.exportComment(outContext)
		outContext.writeln('return self.'+self.getPrivateFieldName())
		outContext.level -= 1

class PyParam(TaxonParam, PyCommonVar):
	def getName(self, user):
		return self.name

	def exportString(self):
		s = self.getName(self)
		expr = self.getValueTaxon()
		if expr:
			s += ' ' + expr.exportString()
		return s
