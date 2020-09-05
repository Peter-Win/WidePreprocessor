from core.TaxonOverload import TaxonOverload
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyOverload(TaxonOverload):
	def exportLexems(self, level, lexems, style):
		for taxon in self.items:
			taxon.exportLexems(level, lexems, style)