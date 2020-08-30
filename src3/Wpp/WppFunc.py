from core.TaxonFunc import TaxonFunc
from Wpp.WppTaxon import WppTaxon
from Wpp.body.WppBody import WppBody
from Wpp.WppTypeExpr import WppTypeExpr
from utils.nameCheck import checkLowerCamelCase

class WppFunc(TaxonFunc, WppTaxon):

	validSubTaxons = ('altName', 'param')
	__slots__ = ('headReady')

	def __init__(self, name=''):
		super().__init__(name)
		self.headReady = False

	def checkName(self, name):
		return checkLowerCamelCase(name, self.type)

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
			word = context.getFirstWord()
			if self.isValidSubTaxon(word) or word.startswith('#'):
				return self.readHeadBody(context)
			else:
				self.headReady = True
		return self.getBody().readBody(context)

	def readHeadBody(self, context):
		return super().readBody(context)

	def addTaxon(self, taxon, context):
		if not self.headReady:
			return super().addTaxon(taxon, context)
		return self.getBody().addTaxon(taxon, context)

	def onInit(self):
		if self.isOverload():
			# Еслм функция перегружена, то у нее нельзя использовать дефолтные параметры
			for param in self.getParamsList():
				if param.getValueTaxon():
					param.throwError('It is forbidden to use default parameters for an overloaded function.')
		else:
			# Дефолтные параметры не должны смешиваться с обычными
			prev = None
			for param in self.getParamsList():
				if prev and prev.getValueTaxon() and not param.getValueTaxon():
					prev.throwError('Default parameters should be last.')
				prev = param

	def export(self, outContext):
		# Сначала экспорт заголовка функции
		self.exportHead(outContext)
		typeExpr = self.getResultTypeExpr()
		body = None
		with outContext:
			for item in self.items:
				if item.type == WppBody.type:
					body = item
				elif item != typeExpr:
					item.export(outContext)
		# И в конце тело функции
		body.export(outContext)

	def exportHead(self, outContext):
		parts = [self.type] + self.getExportAttrs() + [self.getName()]
		head = ' '.join(parts)
		typeExpr = self.getResultTypeExpr()
		if typeExpr:
			head += ': ' + typeExpr.exportString()
		outContext.writeln(head)

class WppMethod(WppFunc):
	type = 'method'

class WppConstructor(WppFunc):
	type = 'constructor'
	def getName(self):
		return 'constructor'
	def readHead(self, context):
		words = context.currentLine.split()
		self.attrs = set(words[1:])
		self.setBody(WppBody())
	def isValidSubTaxon(self, taxonType):
		if taxonType == 'autoinit':
			return True
		return super().isValidSubTaxon(taxonType)

	def exportHead(self, outContext):
		parts = [self.type] + self.getExportAttrs()
		outContext.writeln(' '.join(parts))
