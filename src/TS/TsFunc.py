from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor
from TS.TsTaxon import TsTaxon

class TsOverloads(TaxonOverloads):
	def export(self, outContext):
		if len(self.items) != 1:
			self.throwError('TypeScript is not maintains overloaded function '+self.name)
		self.items[0].export(outContext)

class TsCommonFunc(TsTaxon):
	def exportSignature(self):
		""" Parameters + result type """
		s = '(' + ', '.join([p.exportString() for p in self.getParams()]) + ')'
		t = self.getResultType()
		if t:
			s += ': ' + t.exportString()
		return s

class TsFunc(TaxonFunc, TsCommonFunc):
	def export(self, outContext):
		s = 'function ' + self.getName(self)
		if self.getAccessLevel() == 'public':
			s = 'export ' + s
		s += self.exportSignature()
		s += ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')

class TsMethod(TaxonMethod, TsCommonFunc):
	def export(self, outContext):
		s = self.getAccessLevel() + ' '
		if 'static' in self.attrs:
			s += 'static '
		s += self.getName(self) + self.exportSignature() + ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')
		
class TsConstructor(TaxonConstructor, TsCommonFunc):
	def export(self, outContext):
		s = self.getAccessLevel() + ' constructor'
		s += self.exportSignature() + ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')
