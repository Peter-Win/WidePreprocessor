from core.TaxonExpression import TaxonCall, TaxonConst, TaxonBinOp, TaxonFieldExpr, TaxonIdExpr, TaxonNew, TaxonNull, TaxonSuper, TaxonThis, TaxonTernaryOp, TaxonUnOp
from Python.core.PyString import PyString

class PyConst(TaxonConst):
	def exportString(self):
		if self.constType == 'string':
			return PyString.exportConst(self.value)
		return self.value

class PyIdExpr(TaxonIdExpr):
	def exportString(self):
		decl = self.getDeclaration()
		s = decl.getName(self)
		if decl.type == 'Field':
			s = 'self.'+s
		return s

class PyFieldExpr(TaxonFieldExpr):
	def exportString(self):
		return self.id

class PyThis(TaxonThis):
	def exportString(self):
		return 'self'

class PySuper(TaxonSuper):
	def exportString(self):
		return 'super()'

class PyNull(TaxonNull):
	def exportString(self):
		return 'None'

class PyCall(TaxonCall):
	def __init__(self):
		super().__init__()
		self.prior = binOpPrior['.']
	def exportString(self):
		caller = self.getCaller()
		if caller.type == 'Super':
			s = caller.exportString()+'.__init__('
			s += ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
			return s
		else:
			return super().exportString()

class PyNew(TaxonNew):
	def __init__(self):
		super().__init__()
		self.prior = binOpPrior['.']

binOpPrior = {
	'.': 1,
	'**': 10,
	'*': 30, '/': 30, '%': 30, '//': 30,
	'+': 40, '-': 40,
	'>>': 50, '<<': 50,
	'&': 60,
	'^': 70, '|': 70,
	'<=': 80, '<': 80, '>': 80, '>=': 80,
	'==': 90, '!=': 90,
	'=': 100, '%=': 100, '/=': 100, '//=': 100, '-=': 100, '+=': 100, '*=': 100, '**=': 100,
	'is': 110, 'is not': 110,
	'in': 120, 'not in': 120,
	'or': 130, 'and': 130,
}
unOpPrior = {'~': 20, '-': 20, 'not': 130}
ternaryOpPrior = 140

class PyBinOp(TaxonBinOp):
	def onUpdate(self):
		if not self.prior and self.opCode in binOpPrior:
			self.prior = binOpPrior[self.opCode]

	def exportString(self):
		left = self.getLeft()
		right = self.getRight()
		op = self.opCode
		if op != '.':
			op = ' ' + op + ' '
		return self.priorExportString(left) + op + self.priorExportString(right)

class PyTernaryOp(TaxonTernaryOp):
	def __init__(self):
		super().__init__()
		self.prior = ternaryOpPrior

	def exportString(self):
		s = self.priorExportString(self.getPositive())
		s += ' if ' + self.priorExportString(self.getCondition())
		s += ' else ' + self.priorExportString(self.getNegative())
		return s

class PyUnOp(TaxonUnOp):
	def onUpdate(self):
		if not self.prior and self.opCode in unOpPrior:
			self.prior = unOpPrior[self.opCode]
	def exportString(self):
		s = self.opCode
		if s[-1].isalpha():
			s += ' '
		s += self.priorExportString(self.getArgument())
		return s