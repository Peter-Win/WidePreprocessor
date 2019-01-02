from core.TaxonExpression import TaxonConst, TaxonBinOp, TaxonFieldExpr, TaxonIdExpr, TaxonNull, TaxonThis

class PyConst(TaxonConst):
	def exportString(self):
		return self.value

class PyIdExpr(TaxonIdExpr):
	def exportString(self):
		decl = self.getDeclaration()
		return decl.getName(self)

class PyFieldExpr(TaxonFieldExpr):
	def exportString(self):
		return self.id

class PyThis(TaxonThis):
	def exportString(self):
		return 'self'

class PyNull(TaxonNull):
	def exportString(self):
		return 'None'

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

def checkPrior(owner, slave):
	s = slave.exportString()
	if owner.prior < slave.prior:
		s = '(' + s + ')'
	return s

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
		return checkPrior(self, left) + op + checkPrior(self, right)
