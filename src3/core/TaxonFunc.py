"""
Если функция требует перегрузки, то добавляется атрибут overload
"""
from Taxon import Taxon

class TaxonFunc(Taxon):
	type = 'func'
	def getBody(self):
		pass
	def getParamsList(self):
		pass
	def getResultTypeExpr(self):
		pass

	def setBody(self, txBody):
		pass

	def addParam(self, txParam):
		pass

	def setResultTypeExpr(self, txTypeExpr):
		pass