from Taxon import Taxon

class TaxonReturn(Taxon):
	""" Инструкция return. Возможно наличие выражения. Тип выражения должен соответствовать типу функции-владельца """
	__slots__ = ('isAutoChange')
	type = 'Return'

	def __init__(self, name=''):
		super().__init__(name)
		# isAutoChange = данный оператор последний в функции и может быть использован без ключевого слова return
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
