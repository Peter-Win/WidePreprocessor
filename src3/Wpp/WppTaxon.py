from core.TaxonComment import TaxonComment

class WppTaxon:
	extension = 'wpp'

	def addTaxon(self, taxon, context):
		self.checkNewTaxon(taxon, context)
		self.addItem(taxon)
		return taxon

	def readHead(self, context):
		""" 
		 - Эта функция всегда переопределяется в потомках. -
		На момент чтения заголовка еще не инициализированы поля owner и core.
		Поэтому все важные манипуляции нужно вынести в onInit, а здесь парсинг строки.
		Результаты складируются во временные поля таксона, которые уже потом используются в onInit
		"""
		pass

	def readBody(self, context):
		""" В большинстве случаев не требует переопределения, т.к. обычно первое слово в строке - это тип таксона
		Для функций ситуация сложнее, поэтому там функция переопределяется.
		"""
		taxonType = context.getFirstWord()
		if taxonType[0] == '#':
			taxonType = 'comment'
		elif not self.isValidSubTaxon(taxonType):
			context.throwError('Invalid member %s for %s' % (taxonType, self.getDebugStr()))
		taxon = self.creator(taxonType)()
		return taxon

	validSubTaxons = ()
	def isValidSubTaxon(self, taxonType):
		return taxonType in self.validSubTaxons

	def checkNewTaxon(self, taxon, context):
		""" Проверить таксон перед его добавлением """
		from Wpp.WppCore import WppCore
		if taxon.name:
			if taxon.name in WppCore.reservedWords:
				context.throwError('The reserved word "%s" cannot be used as a name' % taxon.name)

			msg = taxon.checkName(taxon.name)
			if msg:
				# Неподходящее имя для таксона. Например, переменные должнв использовать lowerCamelCase
				context.throwError(msg)

			dup = self.findItem(taxon.name)
			if dup:
				# Найден уже существующий элемент с таким же именем
				self.checkDup(taxon, dup, context)

	def checkDup(self, taxon, dup, context):
		context.throwError('Duplicate identifier "%s"' % (taxon.name))

	def getExportAttrs(self):
		res = list(self.attrs)
		res.sort()
		return res

	def exportComments(self, context):
		with context:
			for taxon in self.items:
				if taxon.type == TaxonComment.type:
					taxon.export(context)