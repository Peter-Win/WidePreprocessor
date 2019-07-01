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
		# Нельзя назначать имя типа int. Потому что иначе при поиске в onUpdate он находит сам себя. И происходит зацикливание
		super().__init__('local@' + name)
		self.typeRef = None if not name else Ref(name)

	def getDebugStr(self):
		s = self.typeRef.name if self.typeRef else ('"%s"' % self.name)
		if self.typeRef.target:
			s += '->' + self.typeRef.getDebugStr()
		return s
	def exportString(self):
		return self.typePrefix() + self.typeRef.target.exportString()
	def isReady(self):
		return self.typeRef and self.typeRef.isReady()
	def isReadyFull(self):
		return self.isReady() and self.typeRef.target.isReadyFull()
	def isType(self):
		return True

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
		if not self.typeRef or not self.typeRef.isReady():
			self.throwError('typeRef is not ready')
		qt = QuasiType.combine(self, self.typeRef.target)
		qt.inst = self.owner	# Ссылка на переменную/параметр/поле, для крторого определен локальный тип. Т.е var x:float; inst->x
		return qt

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
	def isReady(self):
		return self.getItemType().isReady()
	def isReadyFull(self):
		return self.getItemType().isReadyFull()
	def buildQuasiType(self):
		class QuasiArray(QuasiType):
			def getDebugStr(self):
				return 'Array<%s>' % (self.itemType.getDebugStr())
		qt = QuasiArray(self.getArray())
		qt.update(self.attrs)
		qt.itemType = self.getItemType()
		qt.inst = self.owner	# Ссылка на переменную
		return qt
	def getDebugStr(self):
		return ' '.join(self.getExportAttrs()) + ('Array<%s>' % (self.getItemType().getDebugStr()))

class TaxonTypeMap(TaxonLocalType):
	type = 'TypeMap'
	def getMap(self):
		return self.core.dictionary['Map']
	def getKeyType(self):
		return self.items[0]
	def getValueType(self):
		return self.items[1]
	def isReady(self):
		return self.getKeyType().isReady() and self.getValueType().isReady()
	def isReadyFull(self):
		return self.getKeyType().isReadyFull() and self.getValueType().isReadyFull()
	def buildQuasiType(self):
		class QuasiMap(QuasiType):
			def getDebugStr(self):
				return 'Map<%s,%s>' % (self.keyType.getDebugStr(), self.valueType.getDebugStr())
		qt = QuasiMap(self.getMap())
		qt.update(self.attrs)
		qt.keyType = self.getKeyType()
		qt.valueType = self.getValueType()
		qt.inst = self.owner	# Ссылка на переменную
		return qt
	def getDebugStr(self):
		return ' '.join(self.getExportAttrs()) + ('Map<%s,%s>' % (self.getKeyType().getDebugStr(), self.getKeyType().getDebugStr() ))
