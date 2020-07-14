from core.TaxonComment import TaxonComment
from out.lexems import Lex

class TSTaxon:
	def exportComment(self, lexems, style):
		for row in TaxonComment.getComments(self):
			lexems += [Lex.slashes(row), Lex.eol]
		
