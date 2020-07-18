from Taxon import Taxon
from core.TaxonExpression import TaxonExpression

class TaxonReturn(Taxon):
	type = 'return'

	def getResult(self):
		""" Оператор return не обязательно возвращает какой-то результат.
		Если у функции тип void, то результат будет None
		"""
		return self.findByTypeEx(TaxonExpression)

	def setResult(self, txExpression):
		old = self.getResult()
		if old:
			self.removeItem(old)
		self.addItem(txExpression)