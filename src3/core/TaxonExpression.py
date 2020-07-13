from Taxon import Taxon
from core.QuasiType import QuasiType
from core.TaxonRef import TaxonRef

class TaxonExpression(Taxon):
	pass

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

class TaxonNamed(TaxonExpression):
	""" Any named entities: variables, functions, types etc
	Example: var x: int = calc(first) - here calc and first are named expressions
	Не используется поле name, т.к. это не имя данного таксона. Алгоритм поиска должен находить по имени только исходный объект.
	"""
	type = 'named'
	__slots__ = ('targetName')
	def __init__(self, targetName=''):
		super().__init__()
		self.targetName = targetName
		self.addItem(TaxonRef())

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.targetName = src.targetName

	def getDebugStr(self):
		return '->%s' % (self.targetName)

	def getRef(self):
		""" Always returns reference """
		return self.items[0]

	def setTarget(self, targetTaxon):
		""" Назначить ссылку на таксон с соответствующим именем """
		self.getRef().setTarget(targetTaxon)

	def getTarget(self):
		""" can return Npne, if referense is not initialized """
		return self.getRef().getTarget()

	def buildQuasiType(self):
		target = self.getTarget()
		return target.buildQuasiType() if target else None
