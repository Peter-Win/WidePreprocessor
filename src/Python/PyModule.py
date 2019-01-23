from core.TaxonModule import TaxonModule
from Python.PyTaxon import PyTaxon
from Python.PyImport import PyImportBlock

class PyModule(TaxonModule, PyTaxon):
	extension = '.py'
	def __init__(self):
		super().__init__()
		self.createImportBlock(PyImportBlock)
