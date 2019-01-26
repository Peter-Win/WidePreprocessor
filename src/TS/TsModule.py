from core.TaxonModule import TaxonModule
from TS.TsTaxon import TsTaxon
from TS.TsImport import TsImportBlock

class TsModule(TaxonModule, TsTaxon):
	extension = '.ts'
	def __init__(self):
		super().__init__()
		self.createImportBlock(TsImportBlock)
