from Taxon import Taxon

class TaxonExpression(Taxon):
	__slots__ = ('prior')
	def __init__(self):
		super().__init__()
		self.prior = 0

	def priorExportString(self, expr):
		s = expr.exportString()
		if self.prior < expr.prior:
			s = '(' + s + ')'
		return s

	def export(self, outContext):
		""" Используется в блоках. Например this.a = a """
		outContext.writeln(self.exportString())

class TaxonConst(TaxonExpression):
	type = 'Const'
	def __init__(self, constType = None, value = None):
		super().__init__()
		self.constType = constType
		self.value = value

	def clone(self, newCore):
		result = super().clone(newCore)
		result.constType = self.constType
		result.value = self.value
		return result

class TaxonNull(TaxonExpression):
	type = 'Null'

class TaxonTrue(TaxonExpression):
	type = 'True'

class TaxonFalse(TaxonExpression):
	type = 'False'

class TaxonId(TaxonExpression):
	__slots__ = ('id') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	def clone(self, newCore):
		result = super().clone(newCore)
		result.id = self.id
		return result
	def getDeclaration(self):
		return self.refs['decl']
	def getFieldDeclaration(self, name):
		decl = self.getDeclaration()
		return decl.getFieldDeclaration(name)

class TaxonIdExpr(TaxonId):
	type = 'IdExpr'

class TaxonFieldExpr(TaxonId):
	type = 'FieldExpr'

class TaxonOpCode(TaxonExpression):
	__slots__ = ('opCode')
	def clone(self, newCore):
		result = super().clone(newCore)
		result.opCode = self.opCode
		return result

class TaxonUnOp(TaxonOpCode):
	type = 'UnOp'
	def getArgument(self):
		return self.items[0]

class TaxonBinOp(TaxonOpCode):
	type = 'BinOp'
	def getLeft(self):
		return self.items[0]
	def getRight(self):
		return self.items[1]

class TaxonClassRef(TaxonExpression):
	def getClass(self):
		return self.findOwner('Class', True)
	def getFieldDeclaration(self, name):
		myClass = self.getClass()
		return myClass.getFieldDeclaration(name)

class TaxonThis(TaxonClassRef):
	type = 'This'

class TaxonSuper(TaxonClassRef):
	type = 'Super'

class TaxonCall(TaxonExpression):
	type = 'Call'
	def getCaller(self):
		return self.items[0]
	def getArguments(self):
		return self.items[1:]
	def exportString(self):
		s = self.priorExportString(self.getCaller()) + '('
		s += ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s

class TaxonNew(TaxonCall):
	""" new Classname() """
	type = 'New'

class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'
	def getCondition(self):
		return self.items[0]
	def getPositive(self):
		return self.items[1]
	def getNegative(self):
		return self.items[2]

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'

class TaxonArrayValue(TaxonExpression):
	""" example: [1, 2, 3] """
	type = 'ArrayValue'
	def exportString(self):
		return '[' + ', '.join([i.exportString() for i in self.items]) + ']'
