from Taxon import Taxon
from core.Ref import Ref

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
		return True

class TaxonConst(TaxonExpression):
	type = 'Const'
	__slots__ = ('constType', 'value')
	def __init__(self, constType = None, value = None):
		super().__init__()
		self.constType = constType
		self.value = value

	def getDebugStr(self):
		return '%s(%s)' % (self.constType, self.value)

	def getRealValue(self):
		if self.constType == 'int':
			return int(self.value)
		if self.constType == 'float':
			return float(self.value)
		return self.value

	def getQuasiType(self):
		return self.creator('Const')(self.constType, self.value)

class TaxonNull(TaxonExpression):
	type = 'Null'

class TaxonTrue(TaxonExpression):
	type = 'True'
	def getQuasiType(self):
		return self.creator('Const')('bool', 'true')

class TaxonFalse(TaxonExpression):
	type = 'False'
	def getQuasiType(self):
		return self.creator('Const')('bool', 'false')

class TaxonId(TaxonExpression):
	__slots__ = ('id', 'decl', 'typeRef') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	refsList = ('decl', 'typeRef')

	def __init__(self, id = None):
		super().__init__()
		self.id = id
		self.decl = None # Ref
		self.typeRef = None # 

	def getQuasiType(self):
		return self.typeRef

	def getDebugStr(self):
		return self.id

	def isReady(self):
		return self.typeRef
	def isReadyFull(self):
		return self.isReady() and self.typeRef.isReadyFull()

	def getMemberDeclaration(self, name):
		return self.typeRef.getMemberDeclaration(name)

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
		return self.taxon.decl.isReadyFull()
	def exec(self):
		decl = self.taxon.decl.target
		self.taxon.typeRef = decl.getTypeDeclaration() if hasattr(decl, 'getTypeDeclaration') else decl
	def __str__(self):
		return 'TaskSetType(%s)' % (self.taxon.id)

class TaxonIdExpr(TaxonId):
	type = 'IdExpr'
	def onUpdate(self):
		result = super().onUpdate()
		self.decl = Ref(self.id)
		self.decl.find(self)
		self.addTask(TaskSetType())
		return result

class TaxonFieldExpr(TaxonId):
	type = 'FieldExpr'
	def onUpdate(self):
		result = super().onUpdate()
		self.decl = Ref(self.id)
		class SetField:
			def check(self):
				return self.taxon.owner.isReady()
			def exec(self):
				taxon = self.taxon
				binOp = taxon.owner
				left = binOp.getLeft()
				taxon.decl.setTarget(left.getMemberDeclaration(taxon.id))
		self.addTask(SetField())
		return result

class TaxonOpCode(TaxonExpression):
	__slots__ = ('opCode', 'decl', 'typeRef')
	refsList = ('decl')
	excludes = ('typeRef')
	def __init__(self, opCode = None):
		super().__init__()
		self.opCode = opCode
		self.decl = Ref(opCode)
		self.typeRef = None
	def getQuasiType(self):
		return self.typeRef

class TaxonUnOp(TaxonOpCode):
	type = 'UnOp'
	def getArgument(self):
		return self.items[0]
	def getDebugStr(self):
		return '(%s %s)' % (self.opCode, self.getArgument())

class TaxonBinOp(TaxonOpCode):
	type = 'BinOp'
	def getLeft(self):
		return self.items[0]
	def getRight(self):
		return self.items[1]
	def getDebugStr(self):
		return '(%s %s %s)' % (self.getLeft().getDebugStr(), self.opCode, self.getRight().getDebugStr())
	def onUpdate(self):
		result = super().onUpdate()
		class WaitForBoth:
			def check(self):
				return self.taxon.getLeft().isReadyFull() and self.taxon.getRight().isReadyFull()
			def exec(self):
				self.taxon._initType()
		# self.addTask(WaitForBoth())
		self.typeRef = self.findUpEx('int')
		return result

	def _initType(self):
		leftType = self.getLeft().getQuasiType()
		rightType = self.getRight().getQuasiType()
		def cmp(taxon, params):
			return False
		self.decl.setTarget(self.findUpEx({'name': self.opCode, 'cmp': cmp}))
#-----

class TaxonClassRef(TaxonExpression):
	def getClass(self):
		return self.findOwner('Class', True)
	def getMemberDeclaration(self, name):
		myClass = self.getClass()
		return myClass.getMemberDeclaration(name)
	def isDeclaration(self):
		return True
	def getQuasiType(self):
		return self.getClass()

class TaxonThis(TaxonClassRef):
	type = 'This'

class TaxonSuper(TaxonClassRef):
	type = 'Super'

class TaxonCall(TaxonExpression):
	type = 'Call'
	def __init__(self):
		super().__init__()
		self.phase = 0
	def getCaller(self):
		return self.items[0]
	def getArguments(self):
		return self.items[1:]
	def exportString(self):
		s = self.priorExportString(self.getCaller()) + '('
		s += ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s

	def getDeclaration(self):
		return self.refs['decl']

class TaxonNew(TaxonCall):
	""" new Classname() """
	type = 'New'

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
