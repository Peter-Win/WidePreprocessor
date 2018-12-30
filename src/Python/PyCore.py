from core.TaxonModule import TaxonModule

class PyCore(TaxonModule):
	def __init__(self):
		from Python.core.PyTaxonMap import PyTaxonMap
		self.taxonMap = PyTaxonMap