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

class WppIdExpr(TaxonIdExpr, WppExpression):
	def exportString(self):
		return self.id

	def onUpdate(self):
		class TaskWppIdExprDecl:
			def check(self):
				return True
			def exec(self):
				taxon = self.taxon
				decl = taxon.findUpEx(taxon.id)
				taxon.setRef('decl', decl)
		if not self.isDeclaration():
			self.addTask(TaskWppIdExprDecl(), 'decl')
			

class WppFieldExpr(TaxonFieldExpr, WppExpression):
	def __init__(self):
		super().__init__()
		self.step = 0
	def exportString(self):
		return self.id
	def onUpdate(self):
		self.step += 1
		# Привязка полей к их владельцам происходит на втором шаге, т.к. требуется декларация для владельцев, а она заполняется на 1м шаге
		if self.step == 1:
			return True
		if self.step == 2:
			binOp = self.owner
			left = binOp.getLeft()
			self.setRef('decl', left.getFieldDeclaration(self.id))

class WppThis(TaxonThis, WppExpression):
	def exportString(self):
		return 'this'

class WppSuper(TaxonSuper, WppExpression):
	def exportString(self):
		return 'super'

class WppTrue(TaxonTrue, WppExpression):
	def exportString(self):
		return 'true'

class WppFalse(TaxonFalse, WppExpression):
	def exportString(self):
		return 'false'

class WppNull(TaxonNull, WppExpression):
	def exportString(self):
		return 'null'

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
				return self.taxon.getCaller().isDeclaration()
			def exec(self):
				taxon = self.taxon
				decl = taxon.getCaller().getDeclaration()
				# Возможная замена на new
				if decl.type == 'Class':
					taxon.replaceByNew()
				# Найти объявление функции (в том случае, если известен объект вызова)
				if decl.type == 'Overloads':
				 	taxon.addTask(TaskWppCallOver(decl), 'over')
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
	def isQuasiReady(self):
		return self.quasiType != None
	def getQuasiType(self):
		if not self.quasiType:
			self.throwError('Not init quasi type for binOp '+self.opCode)
		return self.quasiType

	def exportString(self):
		op = self.opCode
		if op not in nearBinOps:
			op = ' ' + op + ' '
		return self.priorExportString(self.getLeft()) + op + self.priorExportString(self.getRight())
	def onUpdate(self):
		class TaskWppBinOp:
			def check(self):
				taxon = self.taxon
				return taxon.getRight().isQuasiReady() and taxon.getRight().isQuasiReady()
		class TaskWppPointOp:
			def check(self):
				return self.taxon.getRight().isDeclaration()
			def exec(self):
				self.taxon.setRef('decl', self.taxon.getRight().getDeclaration())
		if self.opCode == '.':
			# Для определения типа нужно извлечь тип правого аргумента (поля)
			self.addTask(TaskWppPointOp(), 'decl')

		return super().onUpdate()


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