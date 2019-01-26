from core.TaxonBlock import TaxonBlock

class TsBlock(TaxonBlock):
	def export(self, outContext):
		outContext.level += 1
		for i in self.items:
			i.export(outContext)
		outContext.level -= 1
