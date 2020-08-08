from core.body.TaxonBody import TaxonBody
from Python.PyTaxon import PyTaxon
from out.lexems import Lex

class PyBody(TaxonBody, PyTaxon):
	def exportLexems(self, level, lexems, style):
		if self.isEmpty():
			self.exportLine(level, lexems, style, [Lex.keyword('pass')])
		else:
			for taxon in self.items:
				taxon.exportLexems(level, lexems, style)