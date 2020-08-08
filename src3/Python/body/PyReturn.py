from core.body.TaxonReturn import TaxonReturn
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyReturn(TaxonReturn, PyTaxon):
	def exportLexems(self, level, lexems, style):
		expr = self.getResult()
		line = [Lex.keyword('return')]
		if expr:
			line.append(Lex.space)
			expr.exportLexems(level, line, style)

		self.exportLine(level, lexems, style, line)