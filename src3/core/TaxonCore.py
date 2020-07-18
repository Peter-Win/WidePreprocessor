from TaxonDict import TaxonDict
from core.TaxonScalar import TaxonScalar
from core.TaxonTypedef import TaxonTypedef
from core.types.TaxonTypeExprName import TaxonTypeExprName

class TaxonCore(TaxonDict):
	type = 'core'
	reservedWords = []

	@classmethod
	def createInstance(cls):
		inst = cls()
		inst.init()
		inst.initAll()
		inst.resolveTasks()
		return inst

	def __init__(self):
		super().__init__()
		self.tasks = []
		self.core = self
		self.root = None
		self.reservedWordsSet = {word for word in self.reservedWords}
		from core.buildCoreTaxonsMap import buildCoreTaxonsMap
		self.taxonMap = buildCoreTaxonsMap()

	def init(self):
		self.createScalar()
		self.createAliases()

	def getSafeName(self, name):
		# Если имя совпало с одним из ключевых слов, то добавить подчерк в конце
		# Это гарантирует уникальность, т.к WPP запрещает использовать подчерки в именах, а в других языках это допустимо.
		return name if name not in self.reservedWordsSet else name + '_'

	def isReservedWord(self, word):
		return False

	def setRoot(self, root):
		self.root = self.addItem(root)
		return self.root

	def getRoot(self):
		return self.root

	def copyRootFrom(self, srcCore):
		""" Копирование проекта из другого сообщества """
		root = srcCore.getRoot().cloneAll(self)
		self.setRoot(root)
		root.initAllRefs()
		root.initAll()
		self.resolveTasks()

	def findByPathExt(self, pathExt):
		pos = 0
		currentTaxon = self
		if pathExt[0] == '@root':
			pos = 1
			currentTaxon = self.getRoot()
		while pos < len(pathExt):
			key = pathExt[pos]
			if type(key) == int:
				# Извлечь следующий таксон по индексу
				currentTaxon = currentTaxon.items[key]
			else:
				# В остальных случаях извлекается по имени
				currentTaxon = currentTaxon.findItem(key)
			pos += 1
		return currentTaxon

	def findUp(self, name, caller):
		""" Ядро ищет только среди непосредственно зарегистрированных по имени элементов.
		Если в ядре указанного имени нет, значит поиск закончился неудачно.
		"""
		return self.findItem(name)


	def addTaxonTask(self, taxon, task):
		self.tasks.append(task)
		task.taxon = taxon

	def resolveTasksIteration(self):
		""" Выполнить все задания в очереди 
		return (changed: bool, newQueue: Tasks[])
		"""
		changed = False
		newQueue = []
		# for task in queue:
		while self.tasks:
			task = self.tasks[0]
			if not task.taxon.isValid():
				changed = True # Таксон стал невалидным - исключить его из очереди
			elif task.check():
				task.exec()
				# Здесь в исходную очередь могут добавиться новые задания
				changed = True
			else:
				newQueue.append(task)
			self.tasks.pop(0)
		return (changed, newQueue)

	def resolveTasks(self):
		while len(self.tasks) > 0:
			changed, newQueue = self.resolveTasksIteration()
			if not changed:
				self.throwError('Task list is not changed.')
			self.tasks = newQueue

	def createScalar(self):
		for props in TaxonScalar.propsList:
			inst = self.creator(TaxonScalar.type)(props)
			self.addItem(inst)

	def createAliases(self):
		from core.TaxonTypeAlias import TaxonTypeAlias
		for name, targetName, attrs in self.typeAliases:
			aliasName = self.aliasesMap[name] if self.aliasesMap else name
			tdef = TaxonTypeAlias(name, aliasName)
			self.addItem(tdef)
			tExpr = self.creator(TaxonTypeExprName.type)()
			tExpr.attrs = attrs
			tExpr.setType(self.findItem(targetName))
			tdef.setType(tExpr)

	typeAliases = [
		# size_t. Тип для описания целочисленных размеров. Например, длина массива. Заимствован из C++. Идентичен unsigned long
		('size_t', 'long', {'unsigned'}),
		('byte', 'int8', {'unsigned'}),
		('uint8', 'int8', {'unsigned'}),
	]
	aliasesMap = None

