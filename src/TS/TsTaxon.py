from Taxon import Taxon

class TsTaxon(Taxon):
	def exportComment(self, outContext):
		lines = self.getCommentLines()
		for s in lines:
			outContext.writeln('//'+s)