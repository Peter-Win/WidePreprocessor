from core.TaxonType import TaxonType
from core.TaxonTypeExpr import TaxonTypeExpr

# First item of typedef is TaxonTypeExpr
# Так же возможны generic-parameters

class TaxonTypedef(TaxonType):
	type = 'typedef'

	def getTypeExpr(self):
		j = 0
		while j < len(self.items) and not isinstance(self.items[j], TaxonTypeExpr):
			j += 1
		return self.items[j] if j < len(self.items) else None

	def setType(self, taxonExpr):
		prevTypeExpr = self.getTypeExpr()
		if prevTypeExpr:
			self.items.remove(prevTypeExpr)
		self.addItem(taxonExpr)

	def buildQuasiType(self):
		return self.getTypeExpr().buildQuasiType()
