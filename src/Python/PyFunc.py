from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor
from Python.PyTaxon import PyTaxon
from functools import reduce

class PyOverloads(TaxonOverloads):
	def export(self, outContext):
		# Разделить на специальные группы (группы используютмя только для проверки, т.к. нарушается порядок следования)
		groups = {}
		for item in self.items:
			if item.type == 'Operator' and item.isUnary():
				key = 'unary'
			elif 'right' in item.attrs:
				key = 'right'
			else:
				key = 'std'
			groups.setdefault(key, []).append(item)
			if len(groups[key]) > 1:
				# Пока не поддерживается перегрузка
				self.throwError('Python is not maintains overloaded function '+self.name)

		for i in self.items:
			i.export(outContext)

class PyCommonFunc(PyTaxon):
	def __init__(self, name = None):
		super().__init__(name)
		self._initsAdded = False

	def export(self, outContext):
		s = 'def ' + self.getName(self) + '('
		sparams = [param.exportString() for param in self.getParams()]
		if self.type != 'Func' and 'static' not in self.attrs:
			sparams.insert(0, 'self')
		s += ', '.join(sparams) + '):'
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		outContext.level -= 1
		self.getBody().export(outContext)

class PyFunc(TaxonFunc, PyCommonFunc):
	pass

class PyMethod(TaxonMethod, PyCommonFunc):
	def export(self, outContext):
		if 'static' in self.attrs:
			outContext.writeln('@staticmethod')
		super().export(outContext)

class PyConstructor(TaxonConstructor, PyCommonFunc):
	def getName(self, user):
		return '__init__'
