from core.body.TaxonIf import TaxonIf
from out.lexems import Lex

class TSIf(TaxonIf):
	def exportLexems(self, lexems, rules):
		struct = self.getStructure()
		for cmd, cond, body in struct:
			if cmd == 'elif':
				lexems += [Lex.keyword('else'), Lex.space, Lex.keyword('if')]
			else:
				lexems.append(Lex.keyword(cmd))
			if cond:
				lexems.append(Lex.bracketBegin)
				cond.exportLexems(lexems, rules)
				lexems.append(Lex.bracketEnd)
			body.exportLexems(lexems, rules)