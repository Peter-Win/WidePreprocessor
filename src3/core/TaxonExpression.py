from Taxon import Taxon
from core.QuasiType import QuasiType
from core.TaxonRef import TaxonRef

class TaxonExpression(Taxon):
	__slots__ = ('prior')
	def __init__(self):
		super().__init__()
		self.prior = 0

class TaxonConst(TaxonExpression):
	type = 'const'
	__slots__ = ('constType', 'value', 'srcValue')
	def __init__(self, constType=None, value=None, srcValue=None):
		super().__init__()
		self.constType = constType	# null, bool, int, float, string
		self.value = value			# the type of value depends on constType
		self.srcValue = srcValue	# string with source value. it useful for float

	def getDebugStr(self):
		return '%s(%s)' % (self.constType, self.srcValue or self.value)

	def buildQuasiType(self):
		return QuasiType(self)

	def isNumber(self):
		return self.constType in ('int', 'fixed', 'float')

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.constType = src.constType
		self.value = src.value
		self.srcValue = src.srcValue

class TaxonThis(TaxonExpression):
	type = 'this'
	def getRef(self):
		""" Always returns reference """
		ref = self.findByType(TaxonRef.type)
		if not ref:
			ref = self.addItem(TaxonRef())
		return ref

	def setTarget(self, targetTaxon):
		""" Назначить ссылку на таксон с соответствующим именем """
		self.getRef().setTarget(targetTaxon)

	def getTarget(self):
		""" can return None, if referense is not initialized """
		return self.getRef().getTarget()

	def buildQuasiType(self):
		target = self.getTarget()
		return target.buildQuasiType() if target else None

class TaxonNamed(TaxonThis):
	""" Any named entities: variables, functions, types etc
	Example: var x: int = calc(first) - here calc and first are named expressions
	Не используется поле name, т.к. это не имя данного таксона. Алгоритм поиска должен находить по имени только исходный объект.
	"""
	type = 'named'
	__slots__ = ('targetName')
	def __init__(self, targetName=''):
		super().__init__()
		self.targetName = targetName

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.targetName = src.targetName

	def getDebugStr(self):
		return '->%s' % (self.targetName)


class TaxonCall(TaxonExpression):
	type = 'call'
	opcode = 'call'
	__slots__ = ('overloadKey')
	def __init__(self):
		super().__init__()
		self.overloadKey = None

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.overloadKey = src.overloadKey

	def getCaller(self):
		return self.items[0]

	def changeCaller(self, caller):
		self.items[0] = caller

	def getArguments(self):
		return self.items[1:]

class TaxonNew(TaxonCall):
	type = 'new'
	opcode = 'new'
		
	def buildQuasiType(self):
		# В отличие от функций, new всегда отдает свой класс, независимо от списка параметров
		return self.getCaller().getTarget().buildQuasiType()

class TaxonMemberAccess(TaxonExpression):
	type = 'dot'
	opcode = '.'
	__slots__ = ('memberName')
	def __init__(self, memberName=''):
		super().__init__()
		self.memberName = memberName

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.memberName = src.memberName

	def getLeft(self):
		return self.items[0]

	def getTarget(self):
		leftQt = self.getLeft().buildQuasiType()
		if not leftQt:
			return None
		#TODO: пока очень простые случаи. Не учитывается наследование. Нужно переделать на findDown
		return leftQt.taxon.findItem(self.memberName)

	def buildQuasiType(self):
		target = self.getTarget()
		return target.buildQuasiType() if target else None

class TaxonBinOp(TaxonExpression):
	""" items
	0: left argument
	1: right argument
	2: (after onInit) reference to operator declaration
	"""
	type = 'binop'
	__slots__ = ('opcode')
	def __init__(self, opcode=''):
		super().__init__()
		self.opcode = opcode

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.opcode = src.opcode

	def getLeft(self):
		return self.items[0]

	def getRight(self):
		return self.items[1]

	def getDeclaration(self):
		if len(self.items) < 3:
			return None
		ref = self.items[2].getTarget()
		return ref

	def buildQuasiType(self):
		decl = self.getDeclaration()
		if not decl:
			return None
		return decl.buildQuasiType(self)
