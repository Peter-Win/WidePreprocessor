from core.TaxonVar import TaxonVar, TaxonField, TaxonReadonly, TaxonParam
from TS.TsTaxon import TsTaxon

class TsCommonVar(TsTaxon):
	def exportString(self):
		field = self.refs.get('field')
		user = field or self;
		s = self.getName(self) + ': ' + user.getLocalType().exportString()
		expr = self.getValueTaxon()
		if expr:
			s += ' = ' + expr.exportString()
		return s

	def export(self, outContext):
		s = self.declarator() + self.exportString() + ';'
		outContext.writeln(s)

	def declarator(self):
		return ''

class TsVar(TaxonVar, TsCommonVar):
	def declarator(self):
		s = ('const' if 'const' in self.attrs else 'let') + ' '
		if self.getAccessLevel() == 'public':
			s = 'export ' + s
		return s

class TsField(TaxonField, TsCommonVar):
	def declarator(self):
		s = self.getAccessLevel() + ' '
		if 'static' in self.attrs:
			s += 'static '
		return s

class TsParam(TaxonField, TsCommonVar):
	def __init__(self):
		super().__init__()
		self._autoInit = False
	def onUpdate(self):
		if not self._autoInit and self.autoInitField():
			self._autoInit = True
			self.insertParamInitCode()
		return super().onUpdate()

class TsReadonly(TaxonReadonly, TsField):
	def declarator(self):
		return super().declarator() + 'readonly '