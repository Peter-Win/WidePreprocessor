from core.TaxonComment import TaxonComment
from out.lexems import Lex

class TSComment(TaxonComment):
	def exportLexems(self, lexems, rules):
		lexems += [Lex.slashes(self.text), Lex.eol]