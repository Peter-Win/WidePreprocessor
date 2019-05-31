from core.ErrorTaxon import ErrorTaxon

class Taxon:
	# Для копирования полей их нужно указать в __slots__.
	__slots__ = ('altName', 'attrs', '_comment', 'core', 'importBlock', 'items', '_location', 'name', 'owner', 'usedTasks')
	# Не копируются те поля, которые начинаются указаны в excludes
	excludes = {'attrs', 'core', 'importBlock', 'items', 'owner', 'usedTasks'}
	refsList = set()
	type = ''

	def __init__(self, name = ''):
		""" Для создания таксонов не надо напрямую вызывать конструктор. Для этого есть метод creator """
		self.altName = ''
		self.attrs = set()
		self._comment = ''
		self.name = name
		self.importBlock = None
		self.items = [] # Непосредственно подчиненные элементы
		self.core = None
		# Для вывода информации об ошибке важно указать точное место
		self._location = None	# tuple(fileName, lineNumber, string)
		self.owner = None
		self.usedTasks = set()

	def creator(self, typeId):
		""" Получить конструктор таксона
		example: varTaxon = self.creator('Var')('variableName')
		 """
		if not self.core:
			self.throwError('Invalid core for %s:%s' % (self.type, self.getDebugStr()))
		return self.core.taxonMap[typeId]

	def trace(self, msg):
		Taxon.Trace(msg)
	@staticmethod
	def Trace(msg):
		# print(msg)
		pass



	def getName(self, user):
		return self.name

	def isClass(self):
		return False
	def isType(self):
		return False

	def getExportAttrs(self):
		""" Получить список атрибутов, отсортированных по имени """
		result = list(self.attrs)
		result.sort()
		return result

	def addItem(self, item, nextItem = None, pos = None):
		item.owner = self
		if nextItem:
			i = self.items.index(nextItem)
			self.items.insert(i, item)
		elif pos != None:
			self.items.insert(pos, item)
		else:
			self.items.append(item)
		if self.core:
			item.core = self.core
			item._setCore()
		return item

	def _setCore(self):
		for i in self.items:
			if i and i.core != self.core:
				i.core = self.core
				i._setCore()

	def addItems(self, items):
		for i in items:
			self.addItem(i)

	def replace(self, newTaxon):
		""" Замена текущего таксона на новый """
		ownerItems = self.owner.items
		pos = ownerItems.index(self)
		ownerItems.pop(pos)
		self.owner.addItem(newTaxon, pos = pos)
		self.invalidate()

	def invalidate(self):
		self.owner = None
	def isValid(self):
		return self.owner != None

	def isDeepContains(self, taxon):
		""" Принадлежит ли указанный таксон иерархии, образованной из текущего """
		while taxon and taxon != self:
			taxon = taxon.owner
		return taxon == self

	def addComment(self, line):
		if self._comment:
			self._comment += '\n'
		self._comment += line

	def getCommentLines(self):
		if not self._comment:
			return []
		return [s for s in self._comment.split('\n')]

	def isRoot(self):
		return not self.owner or self.owner == self.core

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

	def getLocation(self):
		taxon = self
		while taxon.owner and not taxon._location:
			taxon = taxon.owner
		return taxon._location

	def throwError(self, message):
		raise ErrorTaxon(message, self.getLocation())

	def getClonedFields(self):
		fields = set()
		refs = set()
		def toList(value):
			if type(value) != str:
				return value
			return [value]
		for cls in self.__class__.__mro__:
			if hasattr(cls, '__slots__'):
				excludes = set(toList(cls.excludes)) if hasattr(cls, 'excludes') else set()
				refsList = set(toList(cls.refsList)) if hasattr(cls, 'refsList') else set()
				excludes |= refsList
				fields |= set([field for field in toList(cls.__slots__) if field not in excludes])
				refs |= refsList
		return (fields, refs)

	def _clone(self, newCore):
		""" Клонирование таксона и всех его подчиненных в другое сообщество 
		"""
		newTaxon = newCore.taxonMap[self.type]()
		newTaxon.core = newCore
		newTaxon.type = self.type
		fieldsList, refsList = self.getClonedFields()
		for field in fieldsList:
			setattr(newTaxon, field, getattr(self, field))
		for refName in refsList:
			srcRef = getattr(self, refName)
			setattr(newTaxon, refName, srcRef.clone() if srcRef else None)
		for i in self.items:
			n = i._clone(newCore)
			if not n:
				self.throwError('Invalid clone for '+self.getPath())
			newTaxon.addItem(n)
		newTaxon.attrs |= self.attrs
		return newTaxon

	def cloneRoot(self, newCore):
		newRoot = self._clone(newCore)
		newRoot.fullUpdate()
		return newRoot

	def onUpdate(self):
		pass

	def update(self):
		""" Рекурсивный проход, если собственный onUpdate() не вернул True """
		if not self.onUpdate():
			self.updateItems()

	def updateItems(self):
		for i in self.items:
			i.update()

	def fullUpdate(self):
		""" update + resolve tasks queue """
		self._setQueue([])
		self.update()
		while len(self._getQueue()) > 0 :
			changed, newQueue = Taxon.resolveQueue(self._getQueue())
			if not changed and len(newQueue) > 0:
				newQueue[0].taxon.throwError('Dead tasks loop. '+', '.join([str(task) for task in newQueue]))
			self._setQueue(newQueue)


	def getAccessLevel(self, defaultValue = ''):
		for level in ['public', 'private', 'protected']:
			if level in self.attrs:
				return level
		return defaultValue

	def addTask(self, task, taskId = None):
		""" task - объект со следующими свойствами
			taxon: Taxon - таксон, для которого выполняется задание (Заполняется автоматически при вызове addTask)
			check(): bool - имеются ли необходимые условия для выполнения задания
			exec(): void - выполнение задания
		"""
		if taskId:
			# Проверка уникальности
			if taskId in self.usedTasks:
				return
			self.usedTasks.add(taskId)
		task.taxon = self
		# Если задание готово, то выполнить его сразу
		if task.check():
			self.trace('- Task started: %s' % (str(task)))
			task.exec()
			return
		# Поставить звдвние в очередь
		self._getQueue().append(task)

	# Пока используется статическая очередь заданий. Но лучше привязать её к ядру
	def _getQueue(self):
		return Taxon._queue
	def _setQueue(self, queue):
		Taxon._queue = queue
	_queue = []

	@staticmethod
	def resolveQueue(queue):
		""" Выполнить все задания в очереди 
		Для предотвращения вечного цикла используется сторож
		"""
		changed = False
		newQueue = []
		# for task in queue:
		Taxon.Trace('- queue start [%d]' % (len(queue)))
		while queue:
			task = queue[0]
			if not task.taxon.isValid():
				changed = True # Таксон стал невалидным - исключить его из очереди
				Taxon.Trace('- cancel task: %s' % (str(task)))
			elif task.check():
				Taxon.Trace('- ready task: %s' % (str(task)))
				task.exec()
				# Здесь в исходную очередь могут добавиться новые задания
				changed = True
			else:
				Taxon.Trace('- NOT ready task: %s' % (str(task)))
				newQueue.append(task)
			queue.pop(0)
		return (changed, newQueue)

	def _queueStr(self):
		return ', '.join([str(task) for task in self._getQueue()])

	def findOwner(self, type, bException = False):
		taxon = self
		while taxon and taxon.type != type:
			taxon = taxon.owner
		if not taxon and bException:
			self.throwError('Not found owner with type '+type)
		return taxon

	def isMatch(self, params):
		if 'cmp' in params:
			return params['cmp'](self, params)
		if params.get('isModule'):
			return self.name == params['name'] and self.type == 'Module'
		return self.name == params['name'] and self.type != 'Module'

	def findUp(self, fromWho, params):
		""" Поиск с подъёмом вверх.
		params = {'name', 'source', 'isModule'}
		Большинство таксонов могут лишь проверить себя и вызвать поиск владельца
		"""
		if self.isMatch(params):
			return self
		if self.owner:
			return self.owner.findUp(self, params)

	def findUpEx(self, name, fromWho = None):
		""" Поиск обхекта по имени. Если не найден, кидается исключение """
		fromWho = fromWho or self
		result = self.findUp(fromWho, {'name': name, 'source': self})
		if not result:
			self.throwError('Name "%s" is not defined' % (name))
		return result

	def findUpPath(self, path):
		pathList = [s.strip() for s in path.split('.')]
		target = self.findUpEx(pathList[0])
		for s in pathList[1:]:
			nextItem = target.dictionary.get(s)
			if not nextItem:
				self.throwError('Taxon %s doesn\'t contain field "%s"' % (target.getPath(), s))
			target = nextItem
		return target

	def findDown(self, params):
		""" Большинство таксонов не ищут вниз. Только пакеты и модули. """
		return []

	def _findDownRecursive(self, params):
		""" Рекурсивный поиск вниз. Полезен для пакета """
		result = []
		for item in self.items:
			if item.isMatch(params):
				result.append(item)
			else:
				result += item.findDown(params)
		return result
	def _findUpSiblings(self, fromWho, params):
		""" Данный алгоритм подходит для класса """
		if self.isMatch(params):
			return self
		for item in self.items:
			if item != fromWho and item.isMatch(params):
				return item
		if self.owner:
			return self.owner.findUp(self, params)

	def checkAttributes(self, possibleValues=['public', 'private', 'protected']):
		used = []
		for attr in possibleValues:
			if attr in self.attrs:
				used.append(attr)
		if len(used) > 1:
			msg = 'Incompatible attributes used: ' + ', '.join(used)
			self.throwError(msg)

	def addImport(self, targetTaxon):
		""" Вызывается для таксона (элемент выражения, указание на базовый класс) """
		if not targetTaxon:
			return
		# Всплыть до таксона, у которого есть блок импорта. Обычно это модуль.
		taxon = self
		while taxon and not taxon.importBlock:
			taxon = taxon.owner
		if not taxon:
			self.throwError('Not found import block')

		taxon.importBlock.addTaxon(targetTaxon)

	def findModule(self):
		taxon = self
		while taxon and taxon.type != 'Module':
			taxon = taxon.owner
		if not taxon:
			self.throwError('Not found owner module')
		return taxon

	@staticmethod
	def strPack(value):
		lines = value.split('\n')
		return '\n'.join(filter(lambda s: s.strip(), lines))

	def combineAttrs(self, attrs = set()):
		return self.attrs | attrs
