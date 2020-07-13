from core.TaxonTypeExpr import TaxonTypeExpr
from core.QuasiType import QuasiType
from core.TaxonRef import TaxonRef

class TaxonTypeExprName(TaxonTypeExpr):
	type = '@typeExprName'

	def setType(self, txType):
		prevRef = self.getReference()
		if prevRef:
			self.items.remove(prevRef)
		return self.addItem(TaxonRef.fromTaxon(txType))

	def getReference(self):
		j = 0
		while j < len(self.items) and self.items[j].type != TaxonRef.type:
			j += 1
		return self.items[j] if j < len(self.items) else None

	def getTypeTaxon(self):
		tref = self.getReference()
		return tref.getTarget() if tref else None

	def buildQuasiType(self):
		typeTaxon = self.getTypeTaxon()
		return QuasiType.combine(self, typeTaxon) if typeTaxon else None