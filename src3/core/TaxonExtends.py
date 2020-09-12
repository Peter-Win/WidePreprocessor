from Taxon import Taxon
from core.TaxonRef import TaxonRef

class TaxonExtends(Taxon):
	type = 'extends'
	def getRef(self):
		ref = self.findByTypeEx(TaxonRef)
		if not ref:
			ref = self.addItem(TaxonRef())
		return ref

	def setParent(self, parent):
		self.getRef().setTarget(parent)

	def getParent(self):
		return self.getRef().getTarget()

	def isReady(self):
		return self.getParent()