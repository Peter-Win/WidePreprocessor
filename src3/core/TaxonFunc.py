"""
Если функция требует перегрузки, то добавляется атрибут overload
"""
from Taxon import Taxon
from core.body.TaxonBody import TaxonBody
from core.TaxonVar import TaxonParam
from core.TaxonTypeExpr import TaxonTypeExpr

class TaxonFunc(Taxon):
	type = 'func'
	__slots__ = ('paramsMap')

	def __init__(self, name=''):
		super().__init__(name)
		self.paramsMap = None

	def getBody(self):
		return self.findByType(TaxonBody.type)

	def getParamsList(self):
		return [taxon for taxon in self.items if taxon.type == TaxonParam.type]

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
