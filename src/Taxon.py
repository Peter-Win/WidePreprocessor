from core.ErrorTaxon import ErrorTaxon

class Taxon:
	""" Базовый класс для всех остальных элементов иерархии
	Каждый таксон знает своего владельца (owner) и имеет подчиненных (items)
	"""
	type = ''
	canBeStatic = False
	cloneScheme = None
	def __init__(self, name = ''):
		self.owner = None
		self.items = []		# Непосредственно подчиненные элементы
		self.refs = {}		# Ссылки на неподчиненные элементы
		self.name = name
		self.core = None
		# Информация об исходном и полученном таксонах помогают построить перекрестные ссылки
		self.sourceTaxon = None # Когда происходит клонирование, новый таксон сохраняет ссылку на исходный
		# Ссылка на тот таксон, который получен их этого при клонировании
		self.derivedTaxon = None # Эта ссылка перепишется при следующем клонировании
		# Для вывода информации об ошибке важно указать точное место
		self.location = None	# tuple(fileName, lineNumber, string)
		self.attrs = set()
		self.comment = ''
		self.importBlock = None # Возможно наличие объекта TaxonImportBlock
		self.altName = ''

	def getName(self, user):
		return self.name

	def isClass(self):
		return False

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

	def setRef(self, key, item):
		self.refs[key] = item
		item.onRef(self, key)

	def onRef(self, user, key):
		""" Уведомление о том, что некий таксон user ссылается на этот таксон """
		pass

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
		raise ErrorTaxon(message, self.getLocation())

	def getLocation(self):
		taxon = self
		while taxon.owner and not taxon.location:
			taxon = taxon.owner
		return taxon.location

	def clone(self, newCore):
		""" Клонирование таксона и всех его подчиненных в другое сообщество 
		Кроме ссылок, которые могут быть склонированы только после полного копирования всей структуры
		"""
		newTaxon = newCore.taxonMap[self.type]()
		newTaxon.core = newCore
		newTaxon.sourceTaxon = self
		newTaxon.type = self.type
		newTaxon.name = self.name
		newTaxon.location = self.location
		newTaxon.altName = self.altName
		self.derivedTaxon = newTaxon
		for i in self.items:
			n = i.clone(newCore)
			if not n:
				self.throwError('Invalid clone for '+self.getPath())
			newTaxon.addItem(n)
		newTaxon.attrs |= self.attrs
		newTaxon.comment = self.comment
		return newTaxon

	def _findCoreTaxon(self, alienCoreTaxon):
		scheme = alienCoreTaxon.cloneScheme
		if not scheme:
			if self.type == 'Method':
				taxonOwner = self.core.findUp(alienCoreTaxon.owner.owner.name, self.core, self.core)
				taxon = taxonOwner.dictionary[alienCoreTaxon.name]
			else:
				# Если схема не указана, значит поиск глобального объекта по имени
				taxon = self.core.findUp(alienCoreTaxon.name, self.core, self.core)
		elif scheme == 'Owner':
			taxonOwner = self.core.findUp(alienCoreTaxon.owner.name, self.core, self.core)
			if alienCoreTaxon.name not in taxonOwner.dictionary:
				self.throwError('Not found "%s" in %s.%s' % (alienCoreTaxon.name, self.core.name, taxonOwner.name))
			taxon = taxonOwner.dictionary[alienCoreTaxon.name]
		if not taxon:
			self.throwError('Not found "'+alienCoreTaxon.name+':'+alienCoreTaxon.type+'" in "'+self.core.name+'"')
		return taxon

	def updateRefs(self):
		""" Рекурсивное обновление ссылок, необходимое для клонированного объекта
		Типичный сценарий клонирования: сначала dst = src.clone(newCore), затем dst.updateRefs()
		"""
		for key, relatedAlienTaxon in self.sourceTaxon.refs.items():
			relatedFriendlyTaxon = relatedAlienTaxon.derivedTaxon
			if not relatedFriendlyTaxon:
				# Если у исходного таксона нет соответствия в новом сообществе, значит он находится в ядре...
				relatedFriendlyTaxon = self._findCoreTaxon(relatedAlienTaxon)
				relatedAlienTaxon.derivedTaxon = relatedFriendlyTaxon
			self.setRef(key, relatedFriendlyTaxon)

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

	def findUpEx(self, name, fromWho = None):
		""" Поиск обхекта по имени. Если не найден, кидается исключение """
		fromWho = fromWho or self
		result = self.findUp(name, fromWho, fromWho)
		if not result:
			self.throwError('Name "%s" is not defined' % (name))
		return result

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

	def getExportAttrs(self):
		result = list(self.attrs)
		result.sort()
		return result

	def walk(self, onItem):
		onItem(self)
		for item in self.items:
			item.walk(onItem)

	def createImportBlock(self, importBlockClass):
		if not self.importBlock:
			self.importBlock = importBlockClass()

	def addImport(self, targetTaxon):
		""" Вызывается для таксона (элемент выражения, указание на базовый класс) """
		taxon = self
		while taxon and not taxon.importBlock:
			taxon = taxon.owner
		if not taxon:
			self.throwError('Not found import block')
		taxon.importBlock.addImport(targetTaxon)

	def creator(self, typeId):
		return self.core.taxonMap[typeId]

	@staticmethod
	def strPack(value):
		lines = value.split('\n')
		return '\n'.join(filter(lambda s: s.strip(), lines))

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