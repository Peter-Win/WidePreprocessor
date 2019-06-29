from core.TaxonExpression import TaxonArrayIndex, TaxonArrayValue, TaxonBinOp, TaxonConst, TaxonIdExpr, TaxonFieldExpr, TaxonTernaryOp, TaxonThis, TaxonSuper, TaxonUnOp, TaxonTrue, TaxonFalse, TaxonNull, TaxonVoid
from core.TaxonCall import TaxonCall, TaxonNew
from Wpp.expr.parseExpr import slash
from Wpp.WppExpression import WppExpression

revSlash = {value:'\\'+key for key, value in slash.items()}

class WppConst(TaxonConst, WppExpression):
	__slots__ = ()
	def exportString(self):
		if self.constType != 'string':
			return self.value
		s = ''
		for c in self.value:
			s += revSlash.get(c) or c
		return '"'+s+'"'

class WppTrue(TaxonTrue, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'true'

class WppFalse(TaxonFalse, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'false'

class WppNull(TaxonNull, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'null'

class WppVoid(TaxonVoid, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'void'


class WppIdExpr(TaxonIdExpr, WppExpression):
	__slots__ = ()
	def exportString(self):
		return self.id

class WppFieldExpr(TaxonFieldExpr, WppExpression):
	__slots__ = ()
	def exportString(self):
		return self.id

class WppThis(TaxonThis, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'this'

class WppSuper(TaxonSuper, WppExpression):
	__slots__ = ()
	def exportString(self):
		return 'super'

class WppCall(TaxonCall, WppExpression):
	__slots__ = ()
	def _setDecl(self, decl):
		# Возможная замена на new
		if decl.type == 'Class':
			self.replaceByNew(decl)
		else:
			super()._setDecl(decl)

	def replaceByNew(self, decl):
		taxonNew = WppNew()
		for i in self.items:
			taxonNew.addItem(i)
		taxonNew.declTaxon = decl

		self.replace(taxonNew)
		self.trace('WppCall: Replaced %s' % (taxonNew.getDebugStr()))
		
		# Требуется проверить наличие соответствующих конструкторов
		constructorOver = taxonNew.declTaxon.findConstructor()
		if not constructorOver:
			# Если нет конструктора в классе, значит можно вызывать только без параметров - Atom()
			if len(taxonNew.getArguments()) != 0:
				self.throwError('Class %s have no constructor' % (decl.name))
		else:
			constructorOver.find(taxonNew)

class WppNew(TaxonNew, WppExpression):
	__slots__ = ()
	pass

class WppUnOp(TaxonUnOp, WppExpression):
	__slots__ = ()
	def exportString(self):
		return self.opCode + self.priorExportString(self.getArgument())

nearBinOps = {'.'}
class WppBinOp(TaxonBinOp, WppExpression):
	__slots__ = ()
	def __init__(self):
		super().__init__()
		self.quasiType = None

	def exportString(self):
		op = self.opCode
		if op not in nearBinOps:
			op = ' ' + op + ' '
		return self.priorExportString(self.getLeft()) + op + self.priorExportString(self.getRight())
	def onUpdate(self):
		class CheckStatic:
			""" Проверка использования статических полей с классом """
			def check(self):
				binOp = self.taxon
				return binOp.getLeft().isReady() and binOp.getRight().isReady()
			def exec(self):
				taxon = self.taxon
				left = taxon.getLeft()
				isLeftClass =  left.refDecl.target.isClass() if hasattr(left, 'refDecl') else False
				rightDecl = taxon.getRight().refDecl.target
				isRightStatic = 'static' in rightDecl.attrs
				if isLeftClass and not isRightStatic:
					taxon.throwError('Non-static member "%s" cannot be applied to class' % (rightDecl.name))
				if not isLeftClass and isRightStatic:
					taxon.throwError('Static member "%s" can be applied to class only' % (rightDecl.name))
			def __str__(self):
				return 'CheckStatic %s' % (self.taxon.getDebugStr())
		res = super().onUpdate()
		if self.opCode == '.':
			self.addTask(CheckStatic())
		return res


class WppTernaryOp(TaxonTernaryOp, WppExpression):
	__slots__ = ()
	def exportString(self):
		div = [' ? ', ' : ', '']
		res = ''
		for j, item in enumerate(self.items):
			res += self.priorExportString(item)
			res += div[j]
		return res

class WppArrayIndex(TaxonArrayIndex, WppExpression):
	__slots__ = ()
	def exportString(self):
		return '%s[%s]' % (self.getArrayInstance().exportString(), self.getIndexTaxon().exportString())
	def _checkIndexType(self):
		""" Индекс таксона должен каститься в unsigned long """
		# Индексы строгие, как в C++, Java, JS.
		# В PHP отрицательный индекс используется, как ключ ассоциативного массива. В Python - отсчитывает элемент от конца
		# Поэтому для совместимости все индексы беззнаковые целые
		from core.TaxonScalar import TaxonScalar
		from core.QuasiType import QuasiType
		requiredType = TaxonScalar.createByName('long')
		requiredType.attrs.add('unsigned')
		code, errMsg = QuasiType.matchTaxons(requiredType, self.getIndexTaxon())
		if errMsg:
			self.throwError(errMsg)
	def onUpdate(self):
		result = super().onUpdate()
		# Проконтролировать тип индекса. Используется только для Wpp
		class TestIndex:
			def check(self):
				return self.taxon.getIndexTaxon().isReadyFull()
			def exec(self):
				self.taxon._checkIndexType()
			def __str__(self):
				return 'TestArrayIndex'
		self.addTask(TestIndex())
		return result

class WppArrayValue(TaxonArrayValue, WppExpression):
	__slots__ = ()
	pass
