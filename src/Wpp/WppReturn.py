from core.TaxonReturn import TaxonReturn
from Wpp.WppTaxon import WppTaxon
from Wpp.WppExpression import WppExpression

class WppReturn(TaxonReturn, WppTaxon):
	@staticmethod
	def createAuto(expression):
		ret = WppReturn()
		ret.addItem(expression)
		ret.isAutoChange = True
		return ret

	def readHead(self, context):
		pair = context.currentLine.split(' ', 1)
		if len(pair) == 2:
			self.addItem(WppExpression.create(pair[1], context))

	def export(self, outContext):
		chunks = []
		if not self.isAutoChange:
			chunks.append('return')
		expr = self.getExpression()
		if expr:
			chunks.append(expr.exportString())
		if len(chunks) > 0:
			outContext.writeln(' '.join(chunks))
