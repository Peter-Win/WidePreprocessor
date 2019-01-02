from Taxon import Taxon

class TaxonExpression(Taxon):
	__slots__ = ('prior')
	def __init__(self):
		super().__init__()
		self.prior = 0

	def priorExportString(self, expr):
		return expr.exportString() #TODO: ...

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

class TaxonId(TaxonExpression):
	__slots__ = ('id') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	def clone(self, newCore):
		result = super().clone(newCore)
		result.id = self.id
		return result

class TaxonIdExpr(TaxonId):
	type = 'IdExpr'
	def getDeclaration(self):
		return self.refs['decl']

class TaxonFieldExpr(TaxonId):
	type = 'FieldExpr'

class TaxonBinOp(TaxonExpression):
	type = 'BinOp'
	__slots__ = ('opCode')
	def getLeft(self):
		return self.items[0]
	def getRight(self):
		return self.items[1]
	def clone(self, newCore):
		result = super().clone(newCore)
		result.opCode = self.opCode
		return result

class TaxonThis(TaxonExpression):
	type = 'This'

class TaxonSuper(TaxonExpression):
	type = 'Super'

class TaxonCall(TaxonExpression):
	type = 'Call'
	def getCaller(self):
		return self.items[0]
	def getArguments(self):
		return self.items[1:]

class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'