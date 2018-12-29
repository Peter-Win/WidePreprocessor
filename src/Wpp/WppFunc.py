from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod
from Wpp.WppBlock import WppBlock
from Wpp.WppTaxon import WppTaxon
from core.ErrorTaxon import ErrorTaxon
from core.TaxonExpression import TaxonExpression

class WppOverloads(TaxonOverloads):
	def export(self, outContext):
		for func in self.items:
			func.export(outContext)

class WppCommonFunc(WppTaxon):
	def addFuncToOwner(self, owner):
		""" Функция добавляется не к указанному владельцу, а в соответствующий объект Overloads """
		over = owner.dictionary.get(self.name)
		if not over:
			over = WppOverloads()
			over.name = self.name
			owner.addNamedItem(over)
			self.copyAttrsToOwner(over)
			over.addItem(self)
		else:
			over.addItem(self)
			self.testAttrs(over)

	attrsUp = ()
	def copyAttrsToOwner(self, over):
		for a in self.attrsUp:
			if a in self.attrs:
				over.attrs.add(a)
	def testAttrs(self, over):
		for a in self.attrsUp:
			if a in over.attrs and a not in self.attrs:
				self.throwError('Expected attribute "'+a+'"')
			if a not in over.attrs and a in self.attrs:
				self.throwError('Attribute "'+a+'" incompatible with previous overloads')

	def readHead(self, context):
		from Wpp.WppType import WppType
		self._phase = 'header'
		# Создать пустой блок
		self.addItem(WppBlock())
		pair = context.currentLine.split(':', 1)
		if len(pair) == 2:
			# Создать тип функции
			self.addItem(WppType.create(pair[1], context))
		chunks = pair[0].split()
		if len(chunks) < 2:
			context.throwError('Expected name of '+self.type)
		self.name = chunks[-1]	# Имя функции
		self.attrs |= set(chunks[1:-1]) # Атрибуты

	def readBody(self, context):
		if self._phase == 'body':
			return self.readFunctionBody(context)
		taxon, ok = self.readFunctionParams(context)
		if not ok:
			try:
				taxon = super().readBody(context)
			except ErrorTaxon:
				self._phase = 'body'
				taxon = self.readFunctionBody(context)
		return taxon

	def readFunctionParams(self, context):
		from Wpp.WppVar import WppParam
		word = context.getFirstWord()
		if word == 'param':
			return WppParam(), True
		return None, False

	def readFunctionBody(self, context):
		return self.getBody().readBody(context)

	def addTaxon(self, taxon):
		if self._phase == 'body':
			return self.getBody().addItem(taxon)
		else:
			return self.addNamedItem(taxon)

	def onUpdate(self):
		if self._phase == 'update':
			return
		self._phase = 'update'		
		self.tryAutoReturn()

	def tryAutoReturn(self):
		""" Возможная автозамена последнего выражения на return """
		from Wpp.WppReturn import WppReturn
		funcType = self.getResultType()
		bodyItems = self.getBody().items
		if funcType and len(bodyItems) > 0:
			lastCmd = bodyItems[-1]
			if isinstance(lastCmd, TaxonExpression):
				#TODO: Здесь надо проверять соответствие типов
				bodyItems.pop()
				self.getBody().addItem(WppReturn.createAuto(lastCmd))

	def export(self, outContext):
		s = ' '.join([self.keyWord] + list(self.attrs) + [self.name])
		t = self.getResultType()
		if t:
			s += ': ' + t.exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		for item in self.getParams():
			item.export(outContext)
		self.getBody().export(outContext)
		outContext.level -= 1

class WppFunc(TaxonFunc, WppCommonFunc):
	keyWord = 'func'

class WppMethod(TaxonMethod, WppCommonFunc):
	keyWord = 'method'
	attrsUp = ('static', 'virtual')
