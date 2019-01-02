from core.TaxonReturn import TaxonReturn

class PyReturn(TaxonReturn):
	def export(self, outContext):
		s = 'return'
		expr = self.getExpression()
		if expr:
			s += ' ' + expr.exportString()
		outContext.writeln(s)
