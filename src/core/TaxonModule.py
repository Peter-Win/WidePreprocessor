from TaxonDictionary import TaxonDictionary

class TaxonModule(TaxonDictionary):
	type = 'Module'

	def findUp(self, name, fromWho, source):
		""" Переопределенная фунция класса Taxon
		Не проверяет имя модуля, т.к. данная функция игнорирует модули
		Прежде чем подняться вверх, проверяются другие члены модуля. Даже не public.
		"""
		for i in self.items:
			if i != fromWho and i.name == name:
				return i
		if self.owner:
			return self.owner.findUp(name, self, source)

	def findDown(self, name):
		""" Модуль позволяет искать вниз только среди public-элементов
		Ниже модуля спускаться нельзя.
		Количество найденных элементов не превышает 1
		Поэтому гораздо быстрее искать через словарь.
		"""
		possible = self.dictionary.get(name)
		if possible and 'public' in possible.attrs:
			return [possible]
		return []
