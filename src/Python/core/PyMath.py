from core.TaxonClass import TaxonClass
from Python.PyTaxon import PyTaxon
from Python.PyImport import PyImportSimple

class PyMath(TaxonClass):
	def __init__(self):
		super().__init__()
		self.name = 'Math'
		for name in ['abs', 'max', 'min', 'sqrt', 'pow', 'round']:
			self.addNamedItem(PyMathFunc(name = name))
		for name in ['cos', 'sin', 'tan', 'asin', 'acos', 'atan', 'log', 'log10', 'degrees', 'radians', 'atan2']:
			self.addNamedItem(PyMathMethod(name = name))
		for name in ['PI', 'E']:
			self.addNamedItem(PyMathConst(name = name))
		self.addNamedItem(PyMathSqr(name = 'sqr'))
	def getName(self, user):
		return 'math'


class PyMathFunc(PyTaxon):
	""" Простые функции, не требующие импорта math """
	type = 'MathFunc'
	def onRef(self, user, key):
		userOwner = user.owner
		if user.type == 'FieldExpr' and userOwner.type == 'BinOp':
			newTaxon = self.core.taxonMap['IdExpr']()
			newTaxon.id = self.name
			newTaxon.setRef(key, self)
			userOwner.replace(newTaxon)
	def getName(self, user):
		return self.name

class PyMathMethod(PyTaxon):
	""" Функции, импортируемые из math """
	def getName(self, user):
		return self.name
	def onRef(self, user, key):
		user.addImport(PyImportSimple('math'))

class PyMathConst(PyTaxon):
	def getName(self, user):
		return self.name.lower()
	def onRef(self, user, key):
		user.addImport(PyImportSimple('math'))

class PyMathSqr(PyMathFunc):
	type = 'MathSqr'
	def onRef(self, user, key):
		userOwner = user.owner
		if user.type == 'FieldExpr' and userOwner.type == 'BinOp':
			# Call
			# +--> BinOp(.)
			# |    +--> Math
			# |    +--> sqr
			# +--> arg
			callOwner = userOwner.owner
			if callOwner.type == 'Call':
				args = callOwner.getArguments()
				if len(args) == 1:
					newTaxon = self.core.taxonMap['BinOp']()
					newTaxon.opCode = '**'
					newTaxon.addItem(args[0])
					newTaxon.addItem(self.core.taxonMap['Const']('int', '2'))
					callOwner.replace(newTaxon)
					return True
