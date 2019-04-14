class TaxonImportBlock:
	""" Блок импортов.
	Не клонируется, т.к. в каждом языке свои правила импорта
	"""
	def __init__(self, owner):
		self.taxons = set()
		self.owner = owner

	def addTaxon(self, taxon):
		""" Обычеая реакция - проверить принадлежность таксона текущему модулю.
		Если не принадлежит, значит включить
		"""
		if not self.owner.isDeepContains(taxon):
			self.taxons.add(taxon)

	def export(self, outContext):
		pass

	def isEmpty(self):
		return len(self.taxons) == 0

	def groupByModules(self):
		""" Сгруппировать таксоны по модулям
		Это наиболее типичное поведение при экспорте
		Результат: словарь module => [taxon,...]
		"""
		modulesDict = {}
		for taxon in list(self.taxons):
			module = taxon.findModule()
			if module not in modulesDict:
				modulesDict[module] = []
			modulesDict[module].append(taxon)
		return modulesDict