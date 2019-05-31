from Taxon import Taxon
from core.Ref import Ref
from core.QuasiType import QuasiType

class TaxonExpression(Taxon):
	__slots__ = ('prior')
	excludes = ('prior')

	def __init__(self):
		super().__init__()
		self.prior = 0

	def priorExportString(self, expr):
		s = expr.exportString()
		if self.prior < expr.prior:
			s = '(' + s + ')'
		return s

	def getDebugStr(self):
		return self.type

	def isReady(self):
		return True
	def isReadyFull(self):
		# if not self.isReady():
		# 	return False
		# for item in self.items:
		# 	if not item.isReadyFull():
		# 		return False
		return self.isReady()

class TaxonConst(TaxonExpression):
	type = 'Const'
	__slots__ = ('constType', 'value')
	def __init__(self, constType = None, value = None):
		super().__init__()
		self.constType = 'float' if constType=='fixed' else constType
		self.value = value

	def getDebugStr(self):
		return '%s(%s)' % (self.constType, self.value)

	def getRealValue(self):
		if self.constType == 'int':
			return int(self.value)
		if self.constType == 'float':
			return float(self.value)
		return self.value

	def buildQuasiType(self):
		return QuasiType(self)

class TaxonNull(TaxonExpression):
	type = 'Null'

class TaxonVoid(Taxon):
	type = 'Void'
	def isType(self):
		return True
	def getDebudStr(self):
		return 'void'
	def isReady():
		return True
	def isReadyFull():
		return True

class TaxonTrue(TaxonExpression):
	type = 'True'
	def buildQuasiType(self):
		return QuasiType(self)

class TaxonFalse(TaxonExpression):
	type = 'False'
	def buildQuasiType(self):
		return QuasiType(self)

class TaxonId(TaxonExpression):
	__slots__ = ('id', 'refDecl', 'typeTaxon') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	refsList = ('refDecl', 'typeTaxon')

	def __init__(self, id = None):
		super().__init__()
		self.id = id
		self.refDecl = None
		self.typeTaxon = None

	def getDebugStr(self):
		return self.id
	def buildQuasiType(self):
		if not self.typeTaxon:
			self.throwError('Not ready typeTaxon in buildQuasiType')
		return self.typeTaxon.buildQuasiType()

	def isReady(self):
		return self.typeTaxon != None
	def isReadyFull(self):
		return self.isReady() and self.typeTaxon.isReadyFull()

	def getFuncDeclaration(self):
		if not self.refDecl or not self.refDecl.isReady():
			return None
		decl = self.refDecl.target

		from core.TaxonFunc import TaxonCommonFunc
		if decl.type != 'Class' and not isinstance(decl, TaxonCommonFunc):
			from core.debugUtils import recursiveDebugStr
			recursiveDebugStr(self)
			self.throwError('Expected function instead of ' + decl.type)
		return decl
	def getMemberDeclaration(self, name):
		return self.typeTaxon.getMemberDeclaration(name)

	def checkShortStatic(self):
		""" Проверяет, является ли данная конструкция обращением к статическому члему класса без указания класса
		В Wpp такое возможно, но лишь внутри класса. В других языках нужно дописывать класс.
		Если нет, возвращает None. Если да - таксон того класса, которому принадлежит поле
		"""
		decl = self.getDeclaration()
		if decl.type == 'Class':
			return None
		if 'static' not in decl.attrs:
			return None
		ownerClass = decl.findOwner('Class')
		if not ownerClass:
			return None
		# Теперь надо проверить, не является ли правой частью частью бинарного оператора ClassName.member
		owner = self.owner
		if owner.type == 'BinOp' and owner.opCode == '.' and self == owner.getRight():
			leftDecl = owner.getLeft().getDeclaration()
			if leftDecl.type == 'Class':
				return None
		return ownerClass

	def updateShortStatic(self, classTaxon):
		""" Дописать имя класса к обращению к статическому члену. Вызывается из onUpdate если testShortStatic() вернет True """
		binOp = self.core.taxonMap['BinOp']()
		binOp.opCode = '.'
		self.replace(binOp)
		idClass = self.core.taxonMap['IdExpr']()
		field = self.core.taxonMap['FieldExpr']()
		binOp.addItems([idClass, field])
		idClass.id = classTaxon.name
		idClass.setRef('decl', classTaxon)
		field.id = self.id

class TaskSetType:
	def check(self):
		return self.taxon.refDecl.isReadyFull()
	def exec(self):
		decl = self.taxon.refDecl.target
		self.taxon.typeTaxon = decl.getTypeDeclaration() if hasattr(decl, 'getTypeDeclaration') else decl
	def __str__(self):
		return 'TaskSetType(%s) path=%s' % (self.taxon.id, self.taxon.getPath())

class TaxonIdExpr(TaxonId):
	__slots__ = ()
	type = 'IdExpr'
	def onUpdate(self):
		result = super().onUpdate()
		self.refDecl = Ref(self.id)
		self.refDecl.find(self) # Возможно, тут нужно ждать готовности. Например, поиск в классе требует, чтобы были готовые его паренты
		self.addTask(TaskSetType())
		return result

class TaxonFieldExpr(TaxonId):
	__slots__ = ()
	type = 'FieldExpr'
	def getFieldTaxon(self):
		return self

class TaxonOpCode(TaxonExpression):
	__slots__ = ('opCode', 'refDecl', 'typeTaxon')
	refsList = ('refDecl')
	excludes = ('typeTaxon')
	def __init__(self, opCode = None):
		super().__init__()
		self.opCode = opCode
		self.refDecl = Ref(opCode)
		self.typeTaxon = None
	def isReady(self):
		return self.typeTaxon != None
	def isReadyFull(self):
		return self.isReady() and self.typeTaxon.isReadyFull()
	def buildQuasiType(self):
		if not self.typeTaxon:
			self.throwError('Not ready type for (%s)' % self.opCode)
		return self.typeTaxon.buildQuasiType()

class TaxonUnOp(TaxonOpCode):
	__slots__ = ()
	type = 'UnOp'
	def getArgument(self):
		return self.items[0]
	def getDebugStr(self):
		return '(%s %s)' % (self.opCode, self.getArgument())

class TaxonBinOp(TaxonOpCode):
	__slots__ = ()
	type = 'BinOp'
	def getLeft(self):
		return self.items[0]
	def getRight(self):
		return self.items[1]
	def isReadyFull(self): # Возможно, тут нужно ждать только свой typeTaxon
		return self.getLeft().isReadyFull() and self.getRight().isReadyFull()
	def getDebugStr(self):
		return '(%s %s %s)' % (self.getLeft().getDebugStr(), self.opCode, self.getRight().getDebugStr())
	def getFuncDeclaration(self):
		if self.opCode == '.':
			return self.getRight().getFuncDeclaration()
		return super().getFuncDeclaration()
	def onUpdate(self):
		"""
		Если оператор . то он обрабатывается по специальному алгоритму:
		1. Ждать, пока созреет правый операнд.
		2. Достать таксон поля из правого операнда через getFieldTaxon
		3. Вызвать left.getFinalType().onUpdateField(left, field)
		4. Заполнить своё поле типа
		"""
		result = super().onUpdate()
		class WaitForLeft:
			def check(self):
				return self.taxon.getLeft().isReady()
			def exec(self):
				fieldTaxon = self.taxon.getRight().getFieldTaxon()
				left = self.taxon.getLeft()
				leftQuasi = left.buildQuasiType()
				declTaxon, typeTaxon = leftQuasi.taxon.onUpdateField(self.taxon, fieldTaxon)
				self.taxon.typeTaxon = typeTaxon
				fieldTaxon.typeTaxon = typeTaxon
				fieldTaxon.refDecl = Ref(declTaxon.name, declTaxon)

			def __str__(self):
				return 'BinOp.WaitForLeft'

		class WaitForBoth:
			def check(self):
				return self.taxon.getLeft().isReadyFull() and self.taxon.getRight().isReadyFull()
			def exec(self):
				self.taxon._initType()
			def __str__(self):
				return 'BibOp.WaitForBoth(%s)' % (self.taxon.opCode)

		if self.opCode == '.':
			self.addTask(WaitForLeft())
		else:
			self.addTask(WaitForBoth())

		return result

	def _initType(self):
		leftType = self.getLeft().buildQuasiType()
		rightType = self.getRight().buildQuasiType()
		def cmp(taxon, params):
			return taxon.name == params['name']
		over = self.findUpEx({'name': self.opCode, 'cmp': cmp})
		sig = Signature()
		sig.params.append(leftType)
		sig.params.append(rightType)
		self.refDecl.setTarget()
#-----

class TaxonClassRef(TaxonExpression):
	def getClass(self):
		return self.findOwner('Class', True)
	def getMemberDeclaration(self, name):
		myClass = self.getClass()
		return myClass.getMemberDeclaration(name)
	def isDeclaration(self):
		return True
	def buildQuasiType(self):
		return self.getClass().buildQuasiType()

class TaxonThis(TaxonClassRef):
	type = 'This'

class TaxonSuper(TaxonClassRef):
	type = 'Super'


class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'
	def getCondition(self):
		return self.items[0]
	def getPositive(self):
		return self.items[1]
	def getNegative(self):
		return self.items[2]

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'

class TaxonArrayValue(TaxonExpression):
	""" example: [1, 2, 3] """
	type = 'ArrayValue'
	def exportString(self):
		return '[' + ', '.join([i.exportString() for i in self.items]) + ']'
