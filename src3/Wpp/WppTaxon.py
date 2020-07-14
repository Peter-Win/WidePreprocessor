from core.TaxonComment import TaxonComment

class WppTaxon:
	extension = 'wpp'

	def addTaxon(self, taxon):
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

	def getExportAttrs(self):
		res = list(self.attrs)
		res.sort()
		return res

	def exportComments(self, context):
		with context:
			for taxon in self.items:
				if taxon.type == TaxonComment.type:
					taxon.export(context)