from core.TaxonExpression import TaxonArrayIndex, TaxonBinOp, TaxonCall, TaxonConst, TaxonIdExpr, TaxonFieldExpr, TaxonNew, TaxonTernaryOp, TaxonThis, TaxonSuper, TaxonUnOp
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

class WppFieldExpr(TaxonFieldExpr, WppExpression):
	def exportString(self):
		return self.id

class WppThis(TaxonThis, WppExpression):
	def exportString(self):
		return 'this'

class WppSuper(TaxonSuper, WppExpression):
	def exportString(self):
		return 'super'

class WppCall(TaxonCall, WppExpression):
	def __init__(self):
		super().__init__()
		self._newPhase = False
	def onUpdate(self):
		result = super().onUpdate()
		# Возможная замена на new
		caller = self.getCaller()
		if not self._newPhase:
			self._newPhase = True
			result = True
		elif caller.type == 'IdExpr' and caller.getDeclaration().type == 'Class':
			self.replaceByNew()
		return result
	def replaceByNew(self):
		taxonNew = WppNew()
		for i in self.items:
			taxonNew.addItem(i)
		self.replace(taxonNew)

class WppNew(TaxonNew, WppExpression):
	pass

class WppUnOp(TaxonUnOp, WppExpression):
	def exportString(self):
		return self.opCode + self.priorExportString(self.getArgument())

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
