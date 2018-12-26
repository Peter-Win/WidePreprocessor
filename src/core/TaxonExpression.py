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

class TaxonFieldExpr(TaxonExpression):
	type = 'FieldExpr'

class TaxonBinOp(TaxonExpression):
	type = 'BinOp'

class TaxonThis(TaxonExpression):
	type = 'This'

class TaxonCall(TaxonExpression):
	type = 'Call'

class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'