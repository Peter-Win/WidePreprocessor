from Taxon import Taxon
from TaxonDictionary import TaxonDictionary
from core.TaxonBlock import TaxonBlock

class TaxonOverloads(Taxon):
	type = 'Overloads'

class TaxonCommonFunc(TaxonDictionary):
	""" Функция или метод класса
	Всегда имеет тело (первый элемент).
	Может иметь тип результата (второй, если есть)
	И параметры, которые доступны через dictionary
	"""

	def getBody(self):
		""" Тело функции присутствует всегда"""
		return self.items[0]

	def getResultType(self):
		""" Получить таксон типа функции. Может вернуть None, если функция не возвращает результат. """
		from core.TaxonType import TaxonType
		# Тип результата (если есть) стоит первым в списке
		hasResult = len(self.items) > 1 and isinstance(self.items[1], TaxonType)
		return self.items[1] if hasResult else None

	def getParams(self):
		""" Линейный список параметров. А для доступа по имени лучше использовать dictionary """
		start = 2 if self.getResultType() else 1
		return self.items[start:]

class TaxonFunc(TaxonCommonFunc):
	type = 'Func'

class TaxonMethod(TaxonCommonFunc):
	type = 'Method'
