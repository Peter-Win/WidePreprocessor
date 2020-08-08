from core.body.TaxonIf import TaxonIf
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyIf(TaxonIf, PyTaxon):
	def exportLexems(self, level, lexems, rules):
		struct = self.getStructure()
		for cmd, cond, body in struct:
			line = [Lex.keyword(cmd)]
			if cond:
				line.append(Lex.space)
				cond.exportLexems(level, line, rules)
				line.append(Lex.colon)
			self.exportLine(level, lexems, rules, line)
			body.exportLexems(level + 1, lexems, rules)