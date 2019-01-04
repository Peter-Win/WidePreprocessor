from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor
from Python.PyTaxon import PyTaxon

class PyOverloads(TaxonOverloads):
	def export(self, outContext):
		if len(self.items) != 1:
			# Пока не поддерживается перегрузка
			self.throwError('Python is not maintains overloaded function')
		self.items[0].export(outContext)

class PyCommonFunc(PyTaxon):
	def __init__(self):
		super().__init__()
		self._initsAdded = False

	def export(self, outContext):
		s = 'def ' + self.getName(self) + '('
		sparams = [param.exportString() for param in self.getParams()]
		if self.type != 'Func' and 'static' not in self.attrs:
			sparams.insert(0, 'self')
		s += ', '.join(sparams) + '):'
		outContext.writeln(s)
		self.getBody().export(outContext)

	def onUpdate(self):
		if not self._initsAdded:
			self._initsAdded = True
			if not self.core:
				self.throwError('Empty core')
			taxonMap = self.core.taxonMap
			for param in self.getAutoInits():
				eq = taxonMap['BinOp']()
				eq.opCode = '='
				self.getBody().addItem(eq)
				pt = taxonMap['BinOp']()
				pt.opCode = '.'
				eq.addItem(pt)
				pt.addItem(taxonMap['This']())
				f = taxonMap['FieldExpr']()
				f.id = param.name
				pt.addItem(f)
				v = taxonMap['IdExpr']()
				v.id = param.name
				v.refs['decl'] = param
				eq.addItem(v)
		return super().onUpdate()

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