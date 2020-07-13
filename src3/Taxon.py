from core.ErrorTaxon import ErrorTaxon

class Taxon:
	type = 'unknown'
	__slots__ = ('name', 'owner', 'items', 'attrs', 'core', '_location')

	def __init__(self, name = ''):
		self.name = name
		self.owner = None
		self.items = []
		self.attrs = set()
		self.core = None
		self._location = None	# tuple(fileName, lineNumber, string)

	def getName(self):
		return self.core.getSafeName(self.name)

	def isCore(self):
		return self == self.core

	def isType(self):
		return False

	def isModule(self):
		return False

	def onInit(self):
		""" Вызывается средой после загрузки всего проекта."""
		pass

	def initAll(self):
		self.onInit()
		for item in self.items:
			item.initAll()

	def onInitRef(self):
		pass
	def initAllRefs(self):
		self.onInitRef()
		for item in self.items:
			item.initAllRefs()

	def isCanFindUp(self):
		""" Возможно ли выполнить поиск вверх."""
		return True

	def findUp(self, name):
		""" Поиск вверх осуществляется для простых имен или для первого имени из пути с точками.
		Операция может быть выполнена не всегда. Например, у класса может быть еще не инициализирован родитель или implements.
		"""
		if self.owner:
			return self.owner.findUp(name)
		return None

	def findOwnerByType(self, taxonType):
		""" Поиск владельца с указанным типом, начиная с непосредственного владельца """
		current = self.owner
		while current:
			if current.type == taxonType:
				return current
			current = current.owner
		return None

	def getOwners(self):
		""" Список владельцев. Нулевой элемент - текущий таксон, последний - ядро """
		current = self
		owners = []
		while current:
			owners.append(current)
			if current.isCore():
				break
			current = current.owner
		return owners

	def getPathExt(self):
		""" Получить путь к таксону, который можно использовать для быстрого поиска в другом сообществе """
		owners = self.getOwners()
		owners.reverse()
		path = []
		if len(owners) >= 2 and owners[0].getRoot() == owners[1]:
			# Специальный случай - поиск от корня
			path.append('@root')
			owners = owners[2:]
		else:
			owners = owners[1:]
		return path + [taxon.name if taxon.name else taxon.owner.items.index(taxon) for taxon in owners]


	def addItem(self, item):
		item.owner = self
		self.items.append(item)
		item.setCore(self.core)
		return item

	def isValid(self):
		return True

	def setCore(self, core):
		if not core:
			return
		self.core = core
		for item in self.items:
			item.setCore(core)

	def getDebugStr(self):
		return '%s %s' % (self.type, self.getPath())


	def getPath(self):
		""" Путь от корня в виде строки, разделенной точками """
		taxon = self
		path = []
		while taxon:
			path.append(taxon.name)
			if taxon.isRoot(): break
			taxon = taxon.owner
		path.reverse()
		return '.'.join(path)

	def isRoot(self):
		return self.owner and self.owner.type == 'core'

	def creator(self, typeId):
		""" Получить конструктор таксона
		example: varTaxon = self.creator('Var')('variableName')
		 """
		if not self.core:
			self.throwError('Invalid core for %s:%s' % (self.type, self.getDebugStr()))
		return self.core.taxonMap[typeId]

	def cloneAll(self, dstOwner):
		newInst = self.clone(dstOwner)
		dstOwner.addItem(newInst)
		for item in self.items:
			item.cloneAll(newInst)
		return newInst

	def clone(self, dstOwner):
		newInst = dstOwner.creator(self.type)()
		newInst.copyFieldsFrom(self)
		return newInst

	def copyFieldsFrom(self, src):
		self.name = src.name
		self.attrs |= src.attrs
		self._location = src._location

	def throwError(self, message):
		raise ErrorTaxon(message, self.getLocation())

	def getLocation(self):
		taxon = self
		while taxon.owner and not taxon._location:
			taxon = taxon.owner
		return taxon._location

	@staticmethod
	def strPack(value):
		lines = value.split('\n')
		return '\n'.join(filter(lambda s: s.strip(), lines))

	def addTask(self, task):
		self.core.addTaxonTask(self, task)

	@staticmethod
	def AttrsToStr(attrs):
		res = list(attrs)
		res.sort()
		return ' '.join(res)

	def findItem(self, name):
		j = 0
		while j < len(self.items) and self.items[j].name != name:
			j += 1
		return self.items[j] if j < len(self.items) else None

	def findByType(self, typeName):
		j = 0
		while j < len(self.items) and self.items[j].type != typeName:
			j += 1
		return self.items[j] if j < len(self.items) else None