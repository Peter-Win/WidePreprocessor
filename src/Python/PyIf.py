from core.TaxonIf import TaxonIf
from Python.PyTaxon import PyTaxon

class PyIf(TaxonIf, PyTaxon):
	def export(self, outContext):
		state = 'if'
		for condition, block in self.getCases():
			outContext.writeln(state + ' ' + condition.exportString() + ':')
			block.export(outContext)
			state = 'elif'
		e = self.getElse()
		if e:
			outContext.writeln('else:')
			e.export(outContext)
