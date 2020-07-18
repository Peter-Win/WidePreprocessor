from core.body.TaxonBody import TaxonBody
from out.lexems import Lex

class TSBody(TaxonBody):
	def exportLexems(self, lexems, rules):
		if 'shortForm' in self.attrs:
			# Если используется короткая форма стрелочной функции
			for taxon in self.items:
				taxon.exportLexems(lexems, rules)
			return

		lexems.append(Lex.bodyBegin)
		for taxon in self.items:
			taxon.exportLexems(lexems, rules)
		lexems.append(Lex.bodyEnd)