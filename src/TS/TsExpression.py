from core.TaxonExpression import TaxonArrayValue, TaxonCall, TaxonConst, TaxonBinOp, TaxonFieldExpr, TaxonIdExpr, TaxonNew, TaxonNull, TaxonSuper, TaxonThis, TaxonTernaryOp, TaxonUnOp, TaxonTrue, TaxonFalse
from TS.core.TsString import TsString
from TS.TsTaxon import TsTaxon

class TsExpression(TsTaxon):
	def export(self, outContext):
		outContext.writeln(self.exportString() + ';')

class TsArrayValue(TaxonArrayValue, TsExpression):
	pass

class TsConst(TaxonConst, TsExpression):
	def exportString(self):
		if self.constType == 'string':
			return TsString.exportConst(self.value)
		return self.value

class TsIdExpr(TaxonIdExpr, TsExpression):
	def exportString(self):
		decl = self.getDeclaration()
		s = decl.getName(self)
		if decl.type == 'Field':
			s = 'this.'+s
		return s
	def onUpdate(self):
		cls = self.checkShortStatic()
		if cls:
			self.updateShortStatic(cls)
		return super().onUpdate()

class TsFieldExpr(TaxonFieldExpr, TsExpression):
	def exportString(self):
		decl = self.owner.getLeft().getFieldDeclaration(self.id)
		return decl.getName(self)

class TsThis(TaxonThis, TsExpression):
	def exportString(self):
		return 'this'

class TsSuper(TaxonSuper, TsExpression):
	def exportString(self):
		return 'super'

class TsNull(TaxonNull, TsExpression):
	def exportString(self):
		return 'null'

class TsTrue(TaxonTrue, TsExpression):
	def exportString(self):
		return 'true'

class TsFalse(TaxonFalse, TsExpression):
	def exportString(self):
		return 'false'

class TsCall(TaxonCall, TsExpression):
	def __init__(self):
		super().__init__()
		self.prior = binOpPrior['.']

class TsNew(TaxonNew, TsExpression):
	def __init__(self):
		super().__init__()
		self.prior = binOpPrior['.']
	def exportString(self):
		s = super().exportString()
		caller = self.getCaller()
		if caller.type == 'IdExpr':
			decl = caller.getDeclaration()
			if decl.type == 'Class' and decl.name == 'String' and decl.owner == decl.core:
				return s
		return 'new ' + s

# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence
binOpPrior = {
	'.': 20 - 19,
	'**': 20 - 15,
	'*': 20 - 14,
	'/': 20 - 14,
	'%': 20 - 14,
	'+': 20 - 13,
	'-': 20 - 13,
	'<<': 20 - 12,
	'>>': 20 - 12,
	'>>>': 20 - 12,
	'<': 20 - 11,
	'<=': 20 - 11,
	'>': 20 - 11,
	'>=': 20 - 11,
	'in': 20 - 11,
	'instanceof': 20 - 11,
	'==': 20 - 10,
	'!=': 20 - 10,
	'===': 20 - 10,
	'!==': 20 - 10,
	'&': 20 - 9,
	'^': 20 - 8,
	'|': 20 - 7,
	'&&': 20 - 6,
	'||': 20 - 5,
	'=': 20 - 3,
	'+=': 20 - 3,
	'-=': 20 - 3,
	'**=': 20 - 3,
	'*=': 20 - 3,
	'/=': 20 - 3,
	'%=': 20 - 3,
	'<<=': 20 - 3,
	'>>=': 20 - 3,
	'>>>=': 20 - 3,
	'&=': 20 - 3,
	'^=': 20 - 3,
	'|=': 20 - 3,
}
unOpPrior = {
	'!': 20 - 16,
	'~': 20 - 16,
	'-': 20 - 16,
}
ternaryOpPrior = 20 - 4

binOpCvt = {
	'==': '===',
	'!=': '!==',
}

class TsBinOp(TaxonBinOp, TsExpression):
	def onUpdate(self):
		# newCode = binOpMap.get(self.opCode)
		# if newCode:
		# 	self.opCode = newCode
		if not self.prior and self.opCode in binOpPrior:
			self.prior = binOpPrior[self.opCode]

	def exportString(self):
		left = self.getLeft()
		right = self.getRight()
		op = self.opCode
		if op in binOpCvt:
			op = binOpCvt[op]
		if op != '.':
			op = ' ' + op + ' '
		return self.priorExportString(left) + op + self.priorExportString(right)

class TsUnaryOp(TaxonUnOp, TsExpression):
	def onUpdate(self):
		if not self.prior and self.opCode in unOpPrior:
			self.prior = unOpPrior[self.opCode]
	def exportString(self):
		s = self.opCode
		s += self.priorExportString(self.getArgument())
		return s

class TsTernaryOp(TaxonTernaryOp, TsExpression):
	def __init__(self):
		super().__init__()
		self.prior = ternaryOpPrior

	def exportString(self):
		cond = self.priorExportString(self.getCondition())
		pos = self.priorExportString(self.getPositive())
		neg = self.priorExportString(self.getNegative())
		return '%s ? %s : %s' % (cond, pos, neg)
