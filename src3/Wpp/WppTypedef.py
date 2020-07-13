from core.TaxonTypedef import TaxonTypedef
from Wpp.WppTaxon import WppTaxon
from Wpp.WppTypeExpr import WppTypeExpr

class WppTypedef(TaxonTypedef, WppTaxon):

	def readHead(self, context):
		errMsg, name, attrs, typeExprCode = self.parse(context.currentLine)

		if errMsg:
			context.throwError(errMsg)

		self.name = name
		self.attrs = attrs
		self.items = []
		self.addTaxon(WppTypeExpr.parse(typeExprCode, context))

	@staticmethod
	def parse(code):
		parts = code.split('=', 1)
		if len(parts) != 2:
			return ('Expected "=" for type declaration', None, None, None)
		nameAndAttrs = parts[0]
		typeExprCode = parts[1].strip()
		words = nameAndAttrs.split()
		if len(words) < 2:
			return ('Expected name of %s' % words[0], None, None, None)

		name = words[-1]
		attrs = set(words[1:-1])
		return (None, name, attrs, typeExprCode)

	def export(self, outContext):
		result = ['typedef'] + self.getExportAttrs() + [self.name, '=', self.getTypeExpr().exportString()]
		outContext.writeln(' '.join(result))
