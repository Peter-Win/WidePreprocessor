from core.TaxonReturn import TaxonReturn

class TsReturn(TaxonReturn):
	def export(self, outContext):
		s = 'return'
		expr = self.getExpression()
		if expr:
			s += ' ' + expr.exportString()
		s += ';'
		outContext.writeln(s)
