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
	def onInit(self):
		super().onInit()
		ownerClass = self.findOwnerByType('class')
		if not ownerClass:
			self.throwError('The method must belong to some class')
		ext = ownerClass.getExtends()
		if ext:
			# Необходимо дождаться готовности класса и проверить наличие членов с таким же именем
			class TaskWaitClass:
				def check(self):
					return ownerClass.isReady()
				def exec(self):
					self.taxon.checkDerived(ext.getParent())
			self.addTask(TaskWaitClass())
		else:
			if 'override' in self.attrs:
				self.throwError('The overridden function can only be in derived class')
	def checkDerived(self, ownerClass):
		dup = ownerClass.findMember(self.name)
		if dup:
			# Найден член класса с таким же именем. 
			parent = dup.owner
			if dup.type != 'method':
				# Переопределять можно только методы
				self.throwError('Parent class "%s" already has a %s "%s"' % (parent.name, dup.type, dup.name))
			if 'override' not in self.attrs:
				self.throwError('Parent class "%s" already has a %s "%s". Attribute "override" must be used.' % (parent.name, dup.type, dup.name))
			if not ('virtual' in dup.attrs or 'override' in dup.attrs):
				self.throwError('Parent class "%s" already has a non-virtual method "%s"' % (parent.name, dup.name))
		else:
			if 'override' in self.attrs:
				self.throwError('No virtual function "%s" found in parent classes' % self.name)

class WppOperator(WppMethod):
	type = 'operator'
	def checkName(self, name):
		from core.operators import opcodeMap
		opDef = opcodeMap.get(name)
		if not opDef:
			return 'Invalid operator name "%s"' % name
		code, altName, opType, prior = opDef
		if opType not in ('binop', 'unop'):
			return 'Unable to override "%s" operator' % name
	def getOpcode(self):
		return self.getName()

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

	def onInit(self):
		super().onInit()
		# проверка наличия super
		ownerClass = self.findOwnerByType('class')
		ext = ownerClass.getExtends()
		if ext:
			# Это значит, что класс имеет родителя. То есть, нужен вызов super
			isSuper = False
			body = self.getBody()
			if len(body.items) > 0 and body.items[0].type == 'call':
				isSuper = body.items[0].getCaller().type == 'super'
			if not isSuper:
				self.throwError('"super" must be called in first line')
			
