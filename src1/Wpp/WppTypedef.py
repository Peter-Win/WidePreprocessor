from core.TaxonTypedef import TaxonTypedef
from Wpp.WppTaxon import WppTaxon
from Wpp.WppLocalType import WppLocalType

class WppTypedef(TaxonTypedef, WppTaxon):
	def readHead(self, context):
		# parse string description: typedef Name: localType
		pair = context.currentLine.split(':', 1)
		if len(pair) != 2:
			context.throwError('Expected ":" for %s declaration' % (self.type))
		# get name
		left = pair[0].split()
		if len(left) < 2:
			context.throwError('Expected name of typedef')
		self.name = left[-1]
		self.attrs |= set(left[1:-1])
		# get local type
		self.addItem(WppLocalType.create(pair[1], context))
		self._location = context.createLocation()

	def export(self, outContext):
		right = '%s: %s' % (self.name, self.getLocalType().exportString())
		result = ['typedef'] + self.getExportAttrs() + [right]
		outContext.writeln(' '.join(result))
