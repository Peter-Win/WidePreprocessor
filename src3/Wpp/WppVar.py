"""
var [public] <varName> : <typeExpression> [ = <initialValue]
param [ref|ptr] <paramName: <typeExpression> [ = <defaultValue>]
field [public|private|protected|static] <fieldName> : <typeExpression> [ = <initialValue>]
"""
from core.TaxonVar import TaxonAutoinit, TaxonVar, TaxonField, TaxonParam
from Wpp.WppTypeExpr import WppTypeExpr
from Wpp.WppExpression import WppExpression
from Wpp.WppTaxon import WppTaxon
from core.QuasiType import QuasiType
from utils.nameCheck import checkLowerCamelCase

class WppCommonVar(WppTaxon):
	def commonVarInit(self, context, name, attrs, typeExpr, initialValue = None):
		self.name = name
		self.attrs |= attrs
		txTypeExpr = WppTypeExpr.parse(typeExpr, context)
		self.addItem(txTypeExpr)
		if initialValue != None:
			txValue = WppExpression.parse(initialValue, context)
			self.addItem(txValue)


	def readHead(self, context):
		if len(self.items) != 0:
			context.throwError('Secondary readHead call')
		self._location = context.createLocation()

		errorMsg, name, attrs, typeDescr, valueDescr = self.parseHead(context.currentLine)
		if errorMsg:
			context.throwError(errorMsg)
		else:
			self.commonVarInit(context, name, attrs, typeDescr, valueDescr)

	@staticmethod
	def parseHead(line):
		""" parse string description """
		pair = line.split(':', 1)
		if len(pair) != 2:
			return ('Expected ":" for type declaration', None, None, None, None)
		nameAndAttrs = pair[0]
		typeAndValue = pair[1]
		pair2 = typeAndValue.split('=', 1)
		typeDescr = pair2[0].strip()
		valueDescr = pair2[1].strip() if len(pair2) == 2 else None 
		words = nameAndAttrs.split()
		# parse main part with name and attrs
		if len(words) < 2:
			return ('Expected name of ' + words[0], None, None, None, None)
		name = words[-1]
		attrs = set(words[1:-1])

		return (None, name, attrs, typeDescr, valueDescr)

	def onCommonInit(self):
		txType = self.getTypeTaxon()
		if not txType:
			self.throwError('Type expression is not initialized')

		# Если есть const, значит должно быть выражение, TODO: возможно не для параметра
		txVal = self.getValueTaxon()
		if 'const' in self.attrs and not txVal:
			self.throwError('Expected value of const')

		# Здесь надо ждать готовности, чтобы проверить типы
		if txVal:
			class TaskWait:
				def check(self):
					return txType.buildQuasiType() and txVal.buildQuasiType()
				def exec(self):
					self.taxon.checkType()
			self.addTask(TaskWait())

	def checkType(self):
		left = self.getTypeTaxon()
		right = self.getValueTaxon()
		result, errMsg = QuasiType.matchTaxons(left, right)
		if errMsg:
			self.throwError(errMsg)

	def export(self, outContext):
		result = [self.type] + self.getExportAttrs() + [self.name + ':'] + [self.getTypeTaxon().exportString()]
		val = self.getValueTaxon()
		if val:
			result += ['=', val.exportString()]
		outContext.writeln(' '.join(result))
		self.exportComments(outContext)

	def checkName(self, name):
		return checkLowerCamelCase(name, self.type)

class WppVar(TaxonVar, WppCommonVar):
	def onInit(self):
		self.onCommonInit()

class WppField(TaxonField, WppCommonVar):
	def onInit(self):
		self.onCommonInit()

class WppParam(TaxonParam, WppCommonVar):
	def onInit(self):
		self.onCommonInit()
	def exportString(self):
		return '%s: %s' % (self.getName(), self.getTypeTaxon().exportString())

class WppAutoinit(TaxonAutoinit, WppCommonVar):
	def checkName(self, name):
		return None
	def readHead(self, context):
		""" autoinit name [= value] """
		chunks = context.currentLine.strip().split('=', 1)
		words = chunks[0].split()
		if len(words) < 2:
			context.throwError('Expected name of autoinit')
		# Здесь пока нельзя искать поле в классе, т.к оно еще может быть не считано
		self.name = words[-1]
		self.attrs = set(words[1:-1])
		if len(chunks) == 2:
			self.addItem(WppExpression.parse(chunks[1], context))

	def onInit(self):
		classDecl = self.findOwnerByType('class')
		if not classDecl:
			self.throwError('Class declaration not found for autoinit "%s"' % self.name)
		# Ищем только среди непосредственных членов класса, т.к инициализация членов родительского класса должна выполняться через его конструктор
		fieldDecl = classDecl.findItem(self.name)
		if not fieldDecl:
			self.throwError('Field declaration not found for autoinit "%s"' % self.name)
		if fieldDecl.type != 'field':
			self.throwError('Autoinit should refer to a class field, not a %s.' % fieldDecl.type)
		# Теперь надо подождать готовность типа поля, чтобы его можно было безопасно скопировать
		class TaskFiedReady:
			def check(self):
				return fieldDecl.buildQuasiType()
			def exec(self):
				newTypeExpr = fieldDecl.getTypeTaxon().cloneAll(self.taxon)
				newTypeExpr.initAllRefs()
				newTypeExpr.initAll()
				newTypeExpr.attrs |= self.taxon.attrs
				# Проверить соответствие типа для initialValue
				if self.taxon.getValueTaxon():
					self.taxon.addTask(TaskCheckType())
		class TaskCheckType:
			def check(self):
				self.left = self.taxon.getTypeTaxon().buildQuasiType()
				self.right = self.taxon.getValueTaxon().buildQuasiType()
				return self.left and self.right
			def exec(self):
				res, err = QuasiType.matchTaxons(self.left, self.right)
				if err:
					self.taxon.throwError(err)

		self.addTask(TaskFiedReady())

	def export(self, outContext):
		parts = ['autoinit'] + self.getExportAttrs() + [self.name]
		val = self.getValueTaxon()
		if val:
			parts += ['=', val.exportString()]
		outContext.writeln(' '.join(parts))
