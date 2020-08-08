from out.lexems import Lex
from core.TaxonComment import TaxonComment

class PyTaxon:
	def exportLine(self, level, lexems, rules, line):
		""" line = list of lexems for single line """
		lexems.append(Lex.indent(level, rules))
		lexems += line
		lexems.append(Lex.eol)

	def exportInternalComment(self, level, lexems, rules):
		rows = TaxonComment.getComments(self)
		if len(rows) == 0:
			return
		if len(rows) == 1:
			self.exportLine(level, lexems, rules, [('\"\"\"%s \"\"\"' % rows[0], 'comment')])
			return

		self.exportLine(level, lexems, rules, [('\"\"\"', 'comment')])
		for tx in rows:
			self.exportLine(level, lexems, rules, [(tx, 'comment')])
		self.exportLine(level, lexems, rules, [('\"\"\"', 'comment')])
