from core.TaxonIf import TaxonIf
from TS.TsTaxon import TsTaxon

class TsIf(TaxonIf, TsTaxon):
	def export(self, outContext):
		state = 'if'
		for condition, block in self.getCases():
			outContext.writeln(state + ' (' + condition.exportString() + ') {')
			block.export(outContext)
			state = '} else if'
		e = self.getElse()
		if e:
			outContext.writeln('} else {')
			e.export(outContext)
		outContext.writeln('}')
