from core.TaxonBlock import TaxonBlock

class PyBlock(TaxonBlock):
	def export(self, outContext):
		outContext.level += 1
		mainBlock = self.items
		if len(mainBlock) == 0:
			outContext.writeln('pass')
		else:
			for i in mainBlock:
				i.export(outContext)
		outContext.level -= 1
