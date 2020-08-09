from core.TaxonClass import TaxonClass
from TS.TSTaxon import TSTaxon
from out.lexems import Lex

class TSClass(TaxonClass, TSTaxon):
	def exportLexems(self, lexems, style):
		if self.owner.isModule() and 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		lexems += [Lex.keyword('class'), Lex.space, Lex.className(self.getName())]
		lexems.append(Lex.bodyBegin)
		for taxon in self.items:
			taxon.exportLexems(lexems, style)
		lexems.append(Lex.bodyEnd)