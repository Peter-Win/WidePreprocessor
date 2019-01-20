from core.TaxonTypedef import TaxonTypedef
from Python.PyTaxon import PyTaxon

class PyTypedef(TaxonTypedef, PyTaxon):
	def export(self, outContext):
		pass
	def getDefaultValue(self):
		return self.getTypeTaxon().getDefaultValue()