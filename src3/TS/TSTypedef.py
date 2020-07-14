from core.TaxonTypedef import TaxonTypedef
from TS.TSTaxon import TSTaxon
from out.lexems import Lex

class TSTypedef(TaxonTypedef, TSTaxon):
	def exportLexems(self, lexems, rules):
		self.exportComment(lexems, rules)
		if 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		lexems += [Lex.keyword('type'), Lex.space, Lex.typeName(self.getName()), Lex.binop('=')]
		self.getTypeExpr().exportLexems(lexems, rules)
		lexems.append(Lex.instrDiv)