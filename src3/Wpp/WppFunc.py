from core.TaxonFunc import TaxonFunc
from Wpp.WppTaxon import WppTaxon
from Wpp.body.WppBody import WppBody
from Wpp.WppTypeExpr import WppTypeExpr

class WppFunc(TaxonFunc, WppTaxon):

	validSubTaxons = ('param')
	__slots__ = ('headReady')

	def __init__(self, name=''):
		super().__init__(name)
		self.headReady = False

	@staticmethod
	def parseHead(code):
		""" return errMsg, name, attrs, resultType """
		pair = code.split(':', 1)
		nameAndAttrs = pair[0]
		resultType = pair[1].strip() if len(pair) == 2 else None
		words = nameAndAttrs.split()
		if len(words) < 2:
			return ('Expected name of ' + words[0], None, None, None)
		name = words[-1]
		attrs = set(words[1:-1])
		return (None, name, attrs, resultType)

	def readHead(self, context):
		errMsg, name, attrs, optionalType = WppFunc.parseHead(context.currentLine)
		if errMsg:
			context.throwError(errMsg)
		self.name = name
		self.attrs = attrs
		self.setBody(WppBody())
		if optionalType:
			self.setResultTypeExpr(WppTypeExpr.parse(optionalType, context))

	def readBody(self, context):
		if not self.headReady:
			# Первая стадия - чтение заголовка
			# Используем реализацию предка, пока не возникнет ошибка
			try:
				taxon = super().readBody(context)
				return taxon
			except:
				self.headReady = True
		return self.getBody().readBody(context)

	def addTaxon(self, taxon):
		if not self.headReady:
			return super().addTaxon(taxon)
		return self.getBody().addTaxon(taxon)

	def export(self, outContext):
		# Сначала экспорт заголовка функции
		parts = [self.type] + self.getExportAttrs() + [self.name]
		head = ' '.join(parts)
		typeExpr = self.getResultTypeExpr()
		if typeExpr:
			head += ': ' + typeExpr.exportString()
		outContext.writeln(head)
		with outContext:
			# Затем список параметров
			for p in self.getParamsList():
				p.export(outContext)
		# И в конце тело функции
		self.getBody().export(outContext)