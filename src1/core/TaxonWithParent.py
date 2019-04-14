# Common parent for class and interface
from TaxonDictionary import TaxonDictionary
from core.Ref import Ref

class TaxonWithParent(TaxonDictionary):
	__slots__ = ('parent',)
	excludes = ('parent',)

	def __init__(self, name = ''):
		super().__init__(name)
		self.parent = None

	def isType(self):
		return True

	def isReady(self):
		return self.parent.isReady() if self.parent else True

	def isReadyFull(self):
		""" True, если заполнены ссылки на все паренты
		Строго говоря, поиск любых сущностей по имени можно выполнять только если isReadyFull() == True
		Иначе возникнет ошибка при попытке искать в классе, который ещё не инициализировал ссылки
		"""
		if not self.parent:
			return True
		return self.parent.isReady() and self.parent.target.isReadyFull()

	def getParent(self):
		return self.parent.target if self.parent else None

	def onUpdate(self):
		super().onUpdate()
		if self.parent:
			self.parent.find(self.owner) # от владельца, чтобы не искать среди parent и implements

		# Обработка членов имеет смысл только после подгрузки всех базовых классов.
		# Потому что иначе не будет работать поиск.
		class WaitForReady:
			def check(self):
				return self.taxon.isReadyFull()
			def exec(self):
				self.taxon.updateItems()
			def __str__(self):
				return 'WaitForReady: ' + self.taxon.getPath()
		self.addTask(WaitForReady())


	def findUp(self, fromWho, params):
		result = self.findWithParent(params['name'])
		if result:
			return result
		return super().findUp(self, params)

	def findWithParent(self, name):
		# Сначала проверка себя, затем поиск в словаре, затем поиск в родителе
		if self.name == name:
			return self
		subItem = self.dictionary.get(name)
		if subItem:
			return subItem
		if self.parent:
			if not self.parent.target:
				self.throwError('Find of "%s" in %s with non-ready parent' % (name, self.getPath()));
			return self.parent.target.findWithParent(name)

	def canUpcastTo(self, targetClass):
		""" Можно ли присвоить экземпляр данного класса переменной типа targetClass """
		if self == targetClass:
			return True
		if not self.parent:
			return False
		if not self.parent.isReady():
			self.throwError('Non-ready parent')
		return self.parent.target.canUpcastTo(targetClass)

