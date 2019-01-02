from Taxon import Taxon

class PyTaxon(Taxon):
	def getName(self, user):
		if self.getAccessLevel() != 'public':
			return '__' + self.name
		return self.name

	def exportComment(self, outContext):
		lines = self.getCommentLines()
		for i, line in enumerate(lines):
			s = line
			if i == 0:
				s = '"""' + s
			if i == len(lines) - 1:
				s += ' """'
			outContext.writeln(s)