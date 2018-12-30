from Taxon import Taxon

class PyTaxon(Taxon):
	def exportComment(self, outContext):
		lines = self.getCommentLines()
		for i, line in enumerate(lines):
			s = line
			if i == 0:
				s = '""" ' + s
			if i == len(lines) - 1:
				s += ' """'
			outContext.writeln(s)