from core.ErrorTaxon import ErrorTaxon

class Taxon:
	""" Базовый класс для всех остальных элементов иерархии
	Каждый таксон знает своего владельца (owner) и имеет подчиненных (items)
	"""
	type = ''
	canBeStatic = False
	def __init__(self):
		self.owner = None
		self.items = []		# Непосредственно подчиненные элементы
		self.refs = {}		# Ссылки на неподчиненные элементы
		self.name = ''
		self.core = None
		# Информация об исходном и полученном таксонах помогают построить перекрестные ссылки
		self.sourceTaxon = None # Когда происходит клонирование, новый таксон сохраняет ссылку на исходный
		# Ссылка на тот таксон, который получен их этого при клонировании
		self.derivedTaxon = None # Эта ссылка перепишется при следующем клонировании
		# Для вывода информации об ошибке важно указать точное место
		self.location = None	# tuple(fileName, lineNumber, string)
		self.attrs = set()
		self.comment = ''

	def getName(self, user):
		return self.name

	def addItem(self, item):
		item.owner = self
		item.core = self.core
		self.items.append(item)
		return item

	def addItems(self, items):
		for i in items:
			self.addItem(i)

	def replace(self, newTaxon):
		""" Замена текущего таксона на новый """
		self.owner.addItem(newTaxon)
		items = self.owner.items
		items.pop()
		i = items.index(self)
		items.pop(i)
		items.insert(i, newTaxon)

	def addComment(self, line):
		if self.comment:
			self.comment += '\n'
		self.comment += line
	def getComment(self):
		return self.comment
	def getCommentLines(self):
		if not self.comment:
			return []
		return [s for s in self.comment.split('\n')]

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

	def throwError(self, message):
		raise ErrorTaxon(message, self.location)

	def clone(self, newCore):
		""" Клонирование таксона и всех его подчиненных в другое сообщество 
		Кроме ссылок, которые могут быть склонированы только после полного копирования всей структуры
		"""
		Constructor = newCore.taxonMap[self.type]
		newTaxon = Constructor()
		newTaxon.core = newCore
		newTaxon.sourceTaxon = self
		newTaxon.type = self.type
		newTaxon.name = self.name
		newTaxon.location = self.location
		self.derivedTaxon = newTaxon
		for i in self.items:
			n = i.clone(newCore)
			if not n:
				self.throwError('Invalid clone for '+self.getPath())
			newTaxon.addItem(n)
		newTaxon.attrs |= self.attrs
		newTaxon.comment = self.comment
		return newTaxon

	def updateRefs(self):
		""" Рекурсивное обновление ссылок, необходимое для клонированного объекта
		Типичный сценарий клонирования: сначала dst = src.clone(newCore), затем dst.updateRefs()
		"""
		for key, relatedAlienTaxon in self.sourceTaxon.refs.items():
			relatedFriendlyTaxon = relatedAlienTaxon.derivedTaxon
			if not relatedFriendlyTaxon:
				# Если у исходного таксона нет соответствия в новом сообществе, значит он находится в ядре...
				relatedFriendlyTaxon = self.core.findUp(relatedAlienTaxon.name, self.core, self.core)
				if not relatedFriendlyTaxon:
					self.throwError('Not found "'+relatedAlienTaxon.name+'" in "'+self.core.name+'"')
				relatedAlienTaxon.derivedTaxon = relatedFriendlyTaxon
			self.refs[key] = relatedFriendlyTaxon

		# рекурсивный вызов для подчиненных элементов
		for i in self.items:
			if not i:
				self.throwError('Empty item')
			i.updateRefs()

	def cloneRoot(self, newCore):
		newRoot = self.clone(newCore)
		newRoot.updateRefs()
		newRoot.fullUpdate()
		return newRoot

	def fullUpdate(self):
		""" Выполнение необходимого количества проходов """
		updateCtx = UpdateContext()
		while updateCtx.step < 20:
			# Пока просто ограничивается количество проходов.
			# Позже можно анализировать факт уменьшения количества элементов
			self.update(updateCtx)
			if updateCtx.count == 0:
				return
			updateCtx.nextStep()
		# Если пришли сюда, значит какие-то элементы постоянно возвращают True в onUpdate
		updateCtx.items[0].throwError('Too much True in onUpdate')


	def update(self, updateCtx):
		""" Рекурсивный проход """
		if self.onUpdate():
			updateCtx.addItem(self)
		for i in self.items:
			i.update(updateCtx)


	def onUpdate(self):
		""" Для выполнения дополгительного прохода необходимо вернуть True """
		pass

	def getAccessLevel(self):
		for level in ['public', 'private', 'protected']:
			if level in self.attrs:
				return level

	def findOwner(self, type, bException = False):
		taxon = self
		while taxon and taxon.type != type:
			taxon = taxon.owner
		if not taxon and bException:
			self.throwError('Not found owner with type '+type)
		return taxon

	def findUp(self, name, fromWho, source):
		""" Поиск с подъёмом вверх.
		Большинство таксонов могут лишь проверить себя и вызвать поиск владельца
		"""
		if self.name == name:
			return self
		if self.owner:
			return self.owner.findUp(name, self, source)

	def findDown(self, name):
		""" Большинство таксонов не ищут вниз. Только пакеты и модули. """
		return [] 

	def findClassDeclaration(self, name, bException = False):
		# Сначала найти модуль-владелец
		result = self.findUp(name, self, self)
		if not result and bException:
			self.throwError('Not found class "'+ name +'"')
		return result

	def checkAttributes(self, possibleValues=['public', 'private', 'protected']):
		used = []
		for attr in possibleValues:
			if attr in self.attrs:
				used.append(attr)
		if len(used) > 1:
			msg = 'Incompatible attributes used: ' + ', '.join(used)
			self.throwError(msg)

class UpdateContext:
	step = 0
	items = []
	count = 0
	def nextStep(self):
		self.step += 1
		self.items = []
		self.count = 0
	def addItem(self, item):
		self.count += 1
		if len(self.items) < 10:
			# Нет смысла копить все 
			self.items.append(item)