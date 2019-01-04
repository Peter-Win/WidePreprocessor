from core.TaxonExpression import TaxonConst, TaxonIdExpr, TaxonFieldExpr, TaxonBinOp, TaxonThis, TaxonCall, TaxonTernaryOp, TaxonArrayIndex, TaxonSuper
from Wpp.expr.parseExpr import slash
from Wpp.WppExpression import WppExpression

revSlash = {value:'\\'+key for key, value in slash.items()}

class WppConst(TaxonConst, WppExpression):
	def exportString(self):
		if self.constType != 'string':
			return self.value
		s = ''
		for c in self.value:
			s += revSlash.get(c) or c
		return '"'+s+'"'

class WppIdExpr(TaxonIdExpr, WppExpression):
	def exportString(self):
		return self.id

	def onUpdate(self):
		if 'decl' not in self.refs:
			decl = self.findUp(self.id, self, self)
			if not decl:
				self.throwError('Not found declaration for "'+self.id+'"')
			self.refs['decl'] = decl

class WppThis(TaxonThis, WppExpression):
	def exportString(self):
		return 'this'

class WppSuper(TaxonSuper, WppExpression):
	def exportString(self):
		return 'super'

class WppCall(TaxonCall, WppExpression):
	pass

nearBinOps = {'.'}
class WppBinOp(TaxonBinOp, WppExpression):
	def exportString(self):
		op = self.opCode
		if op not in nearBinOps:
			op = ' ' + op + ' '
		return self.priorExportString(self.getLeft()) + op + self.priorExportString(self.getRight())

class WppTernaryOp(TaxonTernaryOp, WppExpression):
	def exportString(self):
		div = [' ? ', ' : ', '']
		res = ''
		for j, item in enumerate(self.items):
			res += self.priorExportString(item)
			res += div[j]
		return res
