from core.TaxonTypedef import TaxonTypedef
from Wpp.WppTaxon import WppTaxon
from Wpp.WppType import WppType

class WppTypedef(TaxonTypedef, WppTaxon):
	""" typedef public typeName: local-type-declaration """
	def readHead(self, context):
		pair = context.currentLine.split(':', 1)
		if len(pair) != 2:
			context.throwError('Expected ":"')
		words = pair[0].split()
		if len(words) < 2:
			context.throwError('Expected typedef name')
		self.attrs |= set(words[1:-1])
		self.name = words[-1]
		self.addItem(WppType.create(pair[1], context))
		if not self.getAccessLevel():
			self.attrs.add('public')

	def getExportAttrs(self):
		attrs = super().getExportAttrs()
		if 'public' in attrs:
			attrs.remove('public')
		return attrs

	def export(self, outContext):
		chunks = ['typedef'] + self.getExportAttrs() + [self.getName(self)]
		s = ' '.join(chunks) + ': ' + self.getTypeTaxon().exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		outContext.level -= 1