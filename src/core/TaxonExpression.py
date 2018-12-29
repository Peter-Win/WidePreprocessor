from Taxon import Taxon

class TaxonExpression(Taxon):
	pass

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

class TaxonIdExpr(TaxonExpression):
	type = 'IdExpr'
	__slots__ = ('id') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	def getDeclaration(self):
		return self.refs['decl']
	def clone(self, newCore):
		result = super().clone(newCore)
		result.id = self.id

class TaxonFieldExpr(TaxonExpression):
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

class TaxonCall(TaxonExpression):
	type = 'Call'

class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'