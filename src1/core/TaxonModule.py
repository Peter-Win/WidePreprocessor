from TaxonDictionary import TaxonDictionary

class TaxonModule(TaxonDictionary):
	""" Требуется определить функцию exportComment(outContext), переменную класса extension """
	type = 'Module'
	__slots__ = ('importBlock')

	def __init__(self, name = ''):
		super().__init__(name)
		self.importBlock = None

	def findUp(self, fromWho, params):
		return self._findUpSiblings(fromWho, params)

	def findDown(self, params):
		""" Модуль позволяет искать вниз только среди public-элементов
		Ниже модуля спускаться нельзя.
		Количество найденных элементов не превышает 1
		Поэтому гораздо быстрее искать через словарь.
		"""
		if self.isMatch(params):
			return [self]
		name = params['name']
		possible = self.dictionary.get(name)
		if possible and possible.isMatch(params) and 'public' in possible.attrs:
			return [possible]
		return []

	def export(self, outContext):
		writeContext = outContext.createFile(self.name + self.extension)
		self.exportComment(outContext)
		if self.importBlock:
			self.importBlock.export(writeContext)

		for item in self.items:
			item.export(writeContext)
			# Между компонентами модуля вставляется пустая строка
			writeContext.eol()
		writeContext.close()
