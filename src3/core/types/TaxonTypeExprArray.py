from core.TaxonTypeExpr import TaxonTypeExpr

class TaxonTypeExprArray(TaxonTypeExpr):
	"""
	Экземпляр данного выражения имеет один подчиненный таксон, который является другим выражением
	"""
	type = '@typeExprArray'

	def getItemTaxon(self):
		return self.items[0]
