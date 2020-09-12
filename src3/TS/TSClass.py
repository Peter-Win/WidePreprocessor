from core.TaxonClass import TaxonClass
from TS.TSTaxon import TSTaxon
from out.lexems import Lex
from core.TaxonExtends import TaxonExtends

class TSExtends(TaxonExtends):
	def exportLexems(self, lexems, style):
		pass	

class TSClass(TaxonClass, TSTaxon):
	def exportLexems(self, lexems, style):
		if self.owner.isModule() and 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		lexems += [Lex.keyword('class'), Lex.space, Lex.className(self.getName())]
		parent = self.getParent()
		if parent:
			lexems += [Lex.space, Lex.keyword('extends'), Lex.space, Lex.className(parent.getName())]
		lexems.append(Lex.bodyBegin)
		for taxon in self.items:
			taxon.exportLexems(lexems, style)
		lexems.append(Lex.bodyEnd)