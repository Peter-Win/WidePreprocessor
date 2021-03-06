from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor, TaxonOperator
from Wpp.WppBlock import WppBlock
from Wpp.WppTaxon import WppTaxon
from core.ErrorTaxon import ErrorTaxon
from core.TaxonExpression import TaxonExpression

class WppOverloads(TaxonOverloads):
	def export(self, outContext):
		for func in self.items:
			func.export(outContext)

class WppCommonFunc(WppTaxon):
	def __init__(self):
		super().__init__()

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
		defaultAccess = self.getDefaultAccessLevel()
		if defaultAccess and not self.getAccessLevel(): # Если квалификатор доступа не указан, используется defaultAccess
			self.attrs.add(defaultAccess)

	def getDefaultAccessLevel(self):
		return None

	def readBody(self, context):
		if self._phase == 'body':
			return self.readFunctionBody(context)
		taxon, ok = self.readFunctionParams(context)
		if not ok:
			try:
				taxon = super().readBody(context)
				if context.getFirstWord() == 'cloneScheme':
					self.owner.cloneScheme = self.cloneScheme
					self.cloneScheme = None
			except ErrorTaxon:
				self._phase = 'body'
				taxon = self.readFunctionBody(context)
		return taxon

	def readFunctionParams(self, context):
		from Wpp.WppVar import WppParam
		word = context.getFirstWord()
		if word == 'param':
			return WppParam(), True
		# if word == 'altname':
		# 	self.altName = context.currentLine.split()[1]
		# 	return None, True
		return None, False

	def readFunctionBody(self, context):
		return self.getBody().readBody(context)

	def addTaxon(self, taxon):
		if self._phase == 'body':
			return self.getBody().addTaxon(taxon)
		else:
			return self.addNamedItem(taxon)

	def onUpdate(self):
		if self._phase == 'update':
			return
		self._phase = 'update'		
		self.getBody().tryAutoReturn(self.getResultType())

	def export(self, outContext):
		s = (' '.join([self.keyWord] + self.exportAttrs() + [self.getName(self)])).strip()
		t = self.getResultType()
		if t:
			s += ': ' + t.exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		if self.altName:
			outContext.writeln('altname '+self.altName)
		for item in self.getParams():
			item.export(outContext)
		self.getBody().export(outContext)
		outContext.level -= 1

	def exportAttrs(self):
		res = list(self.attrs)
		res.sort()
		defaultAccess = self.getDefaultAccessLevel()
		if defaultAccess and defaultAccess in res:
			res.remove(defaultAccess)
		return res


class WppFunc(TaxonFunc, WppCommonFunc):
	keyWord = 'func'
	attrsUp = ('public', 'private')

class WppMethod(TaxonMethod, WppCommonFunc):
	keyWord = 'method'
	attrsUp = ('static', 'virtual', 'public', 'protected', 'private')
	classMember = True

	def getDefaultAccessLevel(self):
		return 'public'

	def exportAttrs(self):
		res = super().exportAttrs()
		ownerClass = self.findOwner('Class', True)
		if 'static' in ownerClass.attrs:
			# Если класс статический, то не указывать static для членов
			res.remove('static')
		return res

class WppOperator(TaxonOperator, WppCommonFunc):
	""" Если у оператора есть атрибут right то он выполняется для аргументов, находящихся справа, 
	и только в случае, если для левого операнда не определён соответствующий метод.
	Например, операция x + y будет сначала пытаться вызвать x.__add__(y), и только в том случае, если это не получилось, будет пытаться вызвать y.__radd__(x).
	"""
	keyWord = 'operator'
	attrsUp = ('public', 'private')
	classMember = True
	def getDefaultAccessLevel(self):
		return 'public'

class WppConstructor(TaxonConstructor, WppCommonFunc):
	keyWord = 'constructor'
	classMember = True
	def getName(self, user):
		return ''
	def readHead(self, context):
		words = context.currentLine.split()
		self.attrs |= set(words[1:])
		self._phase = 'header'
		self.name = self.key
		# Создать пустой блок
		self.addItem(WppBlock())
		if not self.getAccessLevel():
			self.attrs.add('public')

	def getDefaultAccessLevel(self):
		return 'public'
