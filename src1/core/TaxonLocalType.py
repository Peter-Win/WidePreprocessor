from Taxon import Taxon
from core.Ref import Ref
from core.QuasiType import QuasiType

class TaxonLocalType(Taxon):
	""" Абстрактный класс типа """
	type = 'LocalType'

class TaxonTypeName(TaxonLocalType):
	""" Тип со ссылкой на объект по имени. Может быть класс, встроенный тип, enum, typedef """
	type = 'TypeName'
	__slots__ = ('typeRef')
	refsList = ('typeRef')
	def __init__(self, name = ''):
		super().__init__(name)
		self.typeRef = None
	def getDebugStr(self):
		return self.typeRef.name if self.typeRef else '?'
	def isReady(self):
		return self.typeRef and self.typeRef.isReady()
	def isReadyFull(self):
		return self.isReady() and self.typeRef.target.isReadyFull()

	def onUpdate(self):
		result = super().onUpdate()
		# Привязка типа по имени
		if not self.typeRef:
			self.throwError('Expected typeRef')
		self.typeRef.find(self)
		return result

	def getMemberDeclaration(self, name):
		return self.typeRef.target.getMemberDeclaration(name)
	def buildQuasiType(self):
		return QuasiType.combine(self, self.typeRef.target)

class TaxonTypeArray(TaxonLocalType):
	type = 'TypeArray'
	def getItemType(self):
		return self.items[0]
	def getArray(self):
		return self.core.dictionary['Array']
	def getFieldDeclaration(self, name):
		return self.getArray().getFieldDeclaration(name)
	def getDefaultValue(self):
		return self.getArray().getDefaultValue()

class TaxonTypeMap(TaxonLocalType):
	type = 'TypeMap'
	def getKeyType(self):
		return self.items[0]
	def getValueType(self):
		return self.items[1]