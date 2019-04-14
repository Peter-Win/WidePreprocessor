from core.TaxonExpression import TaxonArrayIndex, TaxonArrayValue, TaxonBinOp, TaxonCall, TaxonConst, TaxonIdExpr, TaxonFieldExpr, TaxonNew, TaxonTernaryOp, TaxonThis, TaxonSuper, TaxonUnOp, TaxonTrue, TaxonFalse, TaxonNull
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

class WppTrue(TaxonTrue, WppExpression):
	def exportString(self):
		return 'true'

class WppFalse(TaxonFalse, WppExpression):
	def exportString(self):
		return 'false'

class WppNull(TaxonNull, WppExpression):
	def exportString(self):
		return 'null'

class WppIdExpr(TaxonIdExpr, WppExpression):
	def exportString(self):
		return self.id

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
	def onUpdate(self):
		class TaskWppCallOver:
			def __init__(self, decl):
				self.decl = decl
			def check(self):
				return self.decl.canFind(self.taxon)
			def exec(self):
				taxon = self.taxon
				taxon.setRef('decl', self.decl.find(taxon))

		class TaskWppCallId:
			def check(self):
				return self.taxon.getCaller().isReady()
			def exec(self):
				taxon = self.taxon
				decl = taxon.getCaller().decl.target
				# Возможная замена на new
				if decl.type == 'Class':
					taxon.replaceByNew()
				# Найти объявление функции (в том случае, если известен объект вызова)
				elif decl.type == 'Overloads':
				 	taxon.addTask(TaskWppCallOver(decl), 'over')
			def __str__(self):
				return 'WppCallId(%s)' % (self.taxon.exportString())
		
		caller = self.getCaller()
		if caller.type == 'IdExpr':
			self.addTask(TaskWppCallId(), 'IdExpr')
		return super().onUpdate()

	def replaceByNew(self):
		taxonNew = WppNew()
		for i in self.items:
			taxonNew.addItem(i)
		self.replace(taxonNew)

class WppNew(TaxonNew, WppCall):
	pass

class WppUnOp(TaxonUnOp, WppExpression):
	def exportString(self):
		return self.opCode + self.priorExportString(self.getArgument())

nearBinOps = {'.'}
class WppBinOp(TaxonBinOp, WppExpression):
	def __init__(self):
		super().__init__()
		self.quasiType = None

	def exportString(self):
		op = self.opCode
		if op not in nearBinOps:
			op = ' ' + op + ' '
		return self.priorExportString(self.getLeft()) + op + self.priorExportString(self.getRight())
	# def onUpdate(self):
	# 	class TaskWppBinOp:
	# 		def check(self):
	# 			taxon = self.taxon
	# 			return taxon.getRight().isQuasiReady() and taxon.getRight().isQuasiReady()
	# 	class TaskWppPointOp:
	# 		def check(self):
	# 			return self.taxon.getRight().isDeclaration()
	# 		def exec(self):
	# 			self.taxon.setRef('decl', self.taxon.getRight().getDeclaration())
	# 	if self.opCode == '.':
	# 		# Для определения типа нужно извлечь тип правого аргумента (поля)
	# 		self.addTask(TaskWppPointOp(), 'decl')

	# 	return super().onUpdate()


class WppTernaryOp(TaxonTernaryOp, WppExpression):
	def exportString(self):
		div = [' ? ', ' : ', '']
		res = ''
		for j, item in enumerate(self.items):
			res += self.priorExportString(item)
			res += div[j]
		return res

class WppArrayValue(TaxonArrayValue, WppExpression):
	pass