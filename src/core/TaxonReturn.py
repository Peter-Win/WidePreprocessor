from Taxon import Taxon

class TaxonReturn(Taxon):
	""" Инструкция return. Возможно наличие выражения. Тип выражения должен соответствовать типу функции-владельца """
	type = 'Return'

	def __init__(self):
		super().__init__()
		self.isAutoChange = False

	def getExpression(self):
		return self.items[0] if len(self.items) == 1 else None