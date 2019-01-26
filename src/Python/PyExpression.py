from core.TaxonExpression import TaxonArrayValue, TaxonCall, TaxonConst, TaxonBinOp, TaxonFieldExpr, TaxonIdExpr, TaxonNew, TaxonNull, TaxonSuper, TaxonThis, TaxonTernaryOp, TaxonUnOp, TaxonTrue, TaxonFalse
from Python.core.PyString import PyString

class PyExpression:
	def export(self, outContext):
		outContext.writeln(self.exportString())

class PyArrayValue(TaxonArrayValue, PyExpression):
	def exportString(self):
		s = '[' + ', '.join([i.exportString() for i in self.items]) + ']'
		return s

class PyConst(TaxonConst, PyExpression):
	def exportString(self):
		if self.constType == 'string':
			return PyString.exportConst(self.value)
		return self.value

class PyIdExpr(TaxonIdExpr, PyExpression):
	def exportString(self):
		decl = self.getDeclaration()
		s = decl.getName(self)
		if decl.type == 'Field':
			s = 'self.'+s
		return s
	def onUpdate(self):
		cls = self.checkShortStatic()
		if cls:
			self.updateShortStatic(cls)
		return super().onUpdate()

class PyFieldExpr(TaxonFieldExpr, PyExpression):
	def exportString(self):
		decl = self.owner.getLeft().getFieldDeclaration(self.id)
		return decl.getName(self)

class PyThis(TaxonThis, PyExpression):
	def exportString(self):
		return 'self'

class PySuper(TaxonSuper, PyExpression):
	def exportString(self):
		return 'super()'

class PyNull(TaxonNull, PyExpression):
	def exportString(self):
		return 'None'

class PyTrue(TaxonTrue, PyExpression):
	def exportString(self):
		return 'True'

class PyFalse(TaxonFalse, PyExpression):
	def exportString(self):
		return 'False'

class PyCall(TaxonCall, PyExpression):
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

class PyNew(TaxonNew, PyExpression):
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

binOpMap = {
	'&&': 'and',
	'||': 'or',
}

class PyBinOp(TaxonBinOp, PyExpression):
	def onUpdate(self):
		newCode = binOpMap.get(self.opCode)
		if newCode:
			self.opCode = newCode
		if not self.prior and self.opCode in binOpPrior:
			self.prior = binOpPrior[self.opCode]

	def exportString(self):
		left = self.getLeft()
		right = self.getRight()
		op = self.opCode
		if op != '.':
			op = ' ' + op + ' '
		return self.priorExportString(left) + op + self.priorExportString(right)

class PyTernaryOp(TaxonTernaryOp, PyExpression):
	def __init__(self):
		super().__init__()
		self.prior = ternaryOpPrior

	def exportString(self):
		s = self.priorExportString(self.getPositive())
		s += ' if ' + self.priorExportString(self.getCondition())
		s += ' else ' + self.priorExportString(self.getNegative())
		return s

class PyUnOp(TaxonUnOp, PyExpression):
	def onUpdate(self):
		if not self.prior and self.opCode in unOpPrior:
			self.prior = unOpPrior[self.opCode]
	def exportString(self):
		s = self.opCode
		if s[-1].isalpha():
			s += ' '
		s += self.priorExportString(self.getArgument())
		return s
