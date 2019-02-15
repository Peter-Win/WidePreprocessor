from Taxon import Taxon

class TaxonReturn(Taxon):
	""" Инструкция return. Возможно наличие выражения. Тип выражения должен соответствовать типу функции-владельца """
	type = 'Return'

	def __init__(self):
		super().__init__()
		self.isAutoChange = False

	def getExpression(self):
		return self.items[0] if len(self.items) == 1 else None

	def getOwnerFunc(self):
		taxon = self
		while taxon.owner.type != 'Overloads':
			taxon = taxon.owner
		return taxon
	def getQuasiType(self):
		fn = self.getOwnerFunc()
		return fn.getResultType()
	def isQuasiReady(self):
		return True		