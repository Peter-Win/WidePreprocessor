from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor
from Python.PyTaxon import PyTaxon

class PyOverloads(TaxonOverloads):
	def export(self, outContext):
		if len(self.items) != 1:
			# Пока не поддерживается перегрузка
			self.throwError('Python is not maintains overloaded function')
		self.items[0].export(outContext)

class PyCommonFunc(PyTaxon):
	def export(self, outContext):
		s = 'def ' + self.getName(self) + '('
		sparams = [param.exportString() for param in self.getParams()]
		if self.type != 'Func' and 'static' not in self.attrs:
			sparams.insert(0, 'self')
		s += ', '.join(sparams) + '):'
		outContext.writeln(s)
		self.getBody().export(outContext)

class PyFunc(TaxonFunc, PyCommonFunc):
	pass

class PyMethod(TaxonMethod, PyCommonFunc):
	pass

class PyConstructor(TaxonConstructor, PyCommonFunc):
	def getName(self, user):
		return '__init__'