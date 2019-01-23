from core.TaxonImport import TaxonImportBlock, TaxonImport

class PyImportBlock(TaxonImportBlock):
	def export(self, outContext):
		records = sorted(self.dict.values(), key = lambda i: i.getKey())
		for i in records:
			i.export(outContext)
		if self.dict:
			outContext.writeln('')

class PyImportSimple(TaxonImport):
	def export(self, outContext):
		outContext.writeln('import '+self.path)