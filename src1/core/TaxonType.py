from Taxon import Taxon
from core.Ref import Ref

class TaxonType(Taxon):
	""" Абстрактный класс типа """
	type = 'Type'

class TaxonTypeName(TaxonType):
	""" Тип со ссылкой на объект по имени. Может быть класс, встроенный тип, enum, typedef """
	type = 'TypeName'
	__slots__ = ('typeRef')
	refsList = ('typeRef')
	def __init__(self, name = ''):
		super().__init__(name)
		self.typeRef = None
	def isReady(self):
		return self.typeRef and self.typeRef.isReady()
	def isReadyFull(self):
		return self.isReady() and self.typeRef.target.isReadyFull()
	def validate(self, valueTaxon, attrs):
		return self.typeRef.target.validate(valueTaxon, attrs | self.attrs)
	def onUpdate(self):
		result = super().onUpdate()
		# Привязка типа по имени
		if not self.typeRef:
			self.throwError('Expected typeRef')
		self.typeRef.find(self)
		return result
	def getFinalType(self, attrs):
		""" Вычисление конечного типа с финальными атрибутами
		Условие выполнения: isReadyFull
		Позволяет учесть случаи typedef.
		Возвращает пару: таксон, атрибуты
		"""
		typeRef = self.typeRef.target
		if hasattr(typeRef, 'getFinalType'):
			return typeRef.getFinalType(self.attrs)
		return typeRef, self.combineAttrs(attrs)
	def getMemberDeclaration(self, name):
		return self.typeRef.target.getMemberDeclaration(name)

class TaxonTypeArray(TaxonType):
	type = 'TypeArray'
	def getItemType(self):
		return self.items[0]
	def getArray(self):
		return self.core.dictionary['Array']
	def getFieldDeclaration(self, name):
		return self.getArray().getFieldDeclaration(name)
	def getDefaultValue(self):
		return self.getArray().getDefaultValue()

class TaxonTypeMap(TaxonType):
	type = 'TypeMap'
	def getKeyType(self):
		return self.items[0]
	def getValueType(self):
		return self.items[1]