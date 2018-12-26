from core.TaxonExpression import TaxonConst, TaxonIdExpr, TaxonFieldExpr, TaxonBinOp, TaxonThis, TaxonCall, TaxonTernaryOp, TaxonArrayIndex
from Wpp.expr.parseExpr import slash

revSlash = {value:'\\'+key for key, value in slash.items()}

class WppConst(TaxonConst):
	def exportString(self):
		if self.constType != 'string':
			return self.value
		s = ''
		for c in self.value:
			s += revSlash.get(c) or c
		return '"'+s+'"'


