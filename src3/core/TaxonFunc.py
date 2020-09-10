"""
Атрибуты
 abstract  Для нестатических методов. Не имеет тела функции.
 const     Для нестатических методов. Означает, что метод не модифицирует никакие поля своего экземпляра
 overload  Применяется для всех типов функций. Обязателен в случае использования перегрузки
 override  Этот метод переопределяет родительский.
 public    - Для функций, находящихся в модуле означает признак экспорта из модуля.
           - Для метода класса - квалификатор доступа.
 static    Статический метод класса
 virtual   Метод может быть переопределен потомками. В отличие от abstract, имеет свою реализацию.
"""
from Taxon import Taxon
from core.body.TaxonBody import TaxonBody
from core.TaxonVar import TaxonParam, TaxonAutoinit
from core.TaxonTypeExpr import TaxonTypeExpr

class TaxonFunc(Taxon):
	type = 'func'
	__slots__ = ('paramsMap', 'overloadKey')

	def __init__(self, name=''):
		super().__init__(name)
		self.paramsMap = None
		self.overloadKey = None

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.overloadKey = src.overloadKey

	def getName(self):
		# Перегруженные функции лишены имени, поэтому нужно брать имя из владельца
		name = self.name if not self.isOverload() else self.owner.name
		return self.transformName(name)

	def getBody(self):
		return self.findByType(TaxonBody.type)

	def getParamsList(self):
		return [taxon for taxon in self.items if taxon.type in {TaxonParam.type, TaxonAutoinit.type}]

	def getResultTypeExpr(self):
		return self.findByTypeEx(TaxonTypeExpr)

	def setBody(self, txBody):
		oldBody = self.getBody()
		if oldBody:
			self.removeItem(oldBody)
		self.addItem(txBody)

	def addParam(self, txParam):
		self.paramsMap = None
		self.addItem(txParam)

	def setResultTypeExpr(self, txTypeExpr):
		oldExpr = self.getResultTypeExpr()
		if oldExpr:
			self.removeItem(oldExpr)
		self.addItem(txTypeExpr)

	def findParam(self, name):
		if not self.paramsMap:
			self.paramsMap = {tx.name:tx for tx in self.getParamsList()}
		return self.paramsMap.get(name)

	def findUp(self, name, caller):
		param = self.findParam(name)
		if param:
			return param
		return super().findUp(name, caller)

	def isOverload(self):
		return 'overload' in self.attrs

	def buildQuasiType(self):
		resultExpr = self.getResultTypeExpr() or self.core.findItem('void')
		return resultExpr.buildQuasiType()

class TaxonMethod(TaxonFunc):
	type = 'method'

class TaxonConstructor(TaxonFunc):
	type = 'constructor'
