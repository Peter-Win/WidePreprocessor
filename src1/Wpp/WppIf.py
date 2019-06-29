from core.TaxonIf import TaxonIf
from Wpp.WppTaxon import WppTaxon

class WppIf(TaxonIf, WppTaxon):
	def __init__(self):
		super().__init__()
		self.phase = ''

	def canAdd(self):
		return self.phase != 'else'

	def readHead(self, context):
		from Wpp.WppExpression import WppExpression
		from Wpp.WppBlock import WppBlock
		pair = context.currentLine.strip().split(' ', 1)
		self.phase = pair[0]
		if self.phase not in {'if', 'elif', 'else'}:
			context.throwError('Invalid phase of "if" statement: "'+self.phase+'"')
		if self.phase != 'else':
			if len(pair) != 2:
				context.throwError('Expected boolean expression')
			expr = WppExpression.create(pair[1], context)
			self.addItem(expr)
		self.addItem(WppBlock())

	def readBody(self, context):
	 	return self.items[-1].readBody(context)

	def addTaxon(self, taxon):
		return self.items[-1].addItem(taxon)

	def export(self, outContext):
		state = 'if'
		for expr, block in self.getCases():
			outContext.writeln(state + ' ' + expr.exportString())
			with outContext:
				block.export(outContext)
			state = 'elif'
		last = self.getElse()
		if last:
			outContext.writeln('else')
			with outContext:
				last.export(outContext)
