from core.TaxonCast import TaxonCast
from Wpp.WppTaxon import WppTaxon
from Wpp.WppType import WppType
from Wpp.WppBlock import WppBlock

class WppCast(TaxonCast, WppTaxon):
	def readHead(self, context):
		pair = context.currentLine.split(':', 1)
		if len(pair) != 2:
			context.throwError('Expected ":" in cast')
		chunks = pair[0].split()
		self.attrs |= set(chunks[1:])
		self.name = context.currentLine.strip()
		self.addItem(WppType.create(pair[1], context))
		self.addItem(WppBlock())
		if not self.getAccessLevel():
			self.attrs.add('public')

	def readBody(self, context):
		return self.getBody().readBody(context)

	def addTaxon(self, taxon):
		return self.getBody().addTaxon(taxon)

	def onUpdate(self):
		self.getBody().tryAutoReturn(self.getLocalType())
		return super().onUpdate()

	def getExportAttrs(self):
		return list(filter(lambda s: s != 'public', super().getExportAttrs()))

	def export(self, outContext):
		s = ' '.join(['cast'] + self.getExportAttrs())
		s += ': ' + self.getLocalType().exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.getBody().export(outContext)
		outContext.level -= 1