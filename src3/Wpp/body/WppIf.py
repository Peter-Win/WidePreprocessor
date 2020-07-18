from core.body.TaxonIf import TaxonIf
from Wpp.body.WppBody import WppBody
from Wpp.WppTaxon import WppTaxon
from Wpp.WppExpression import WppExpression

class WppIf(TaxonIf, WppTaxon):
	def readHead(self, context):
		words = context.currentLine.strip().split(' ', 1)
		cmd = words[0]
		if cmd in ('if', 'elif'):
			if len(words) != 2:
				context.throwError('Expected conditional expression after '+cmd)
			self.addItem(WppExpression.parse(words[1], context))
			self.addItem(WppBody())
			return 
		elif cmd == 'else':
			self.addItem(WppBody())
		else:
			context.throwError('Invalid part of conditional instruction: "%s"' % (cmd))

	def readBody(self, context):
		if len(self.items) == 0 or self.items[-1].type != WppBody.type:
			context.throwError('Required body taxon inside of conditional instruction')
		return self.items[-1].readBody(context)

	def addTaxon(self, taxon):
		return self.items[-1].addTaxon(taxon)

	def export(self, outContext):
		struct = self.getStructure()
		for cmd, expr, body in struct:
			line = '%s %s' % (cmd, expr.exportString()) if expr else cmd
			outContext.writeln(line)
			body.export(outContext)