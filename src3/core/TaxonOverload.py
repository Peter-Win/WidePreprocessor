from functools import reduce
from Taxon import Taxon
from core.QuasiType import QuasiType

class TaxonOverload(Taxon):
	type = 'overload'

	def addItem(self, taxon, pos = -1):
		# При включении в ovrtload функция лишается имени. Иначе появляются проблемы при построении пути getPathExt
		# Компенсация имени производится в TaxonFunc.getName()
		taxon.name = ''
		super().addItem(taxon, pos)

	def getImplementationByKey(self, overloadKey):
		for item in self.items:
			if item.overloadKey == overloadKey:
				return item
		self.throwError('Not found overload key %s' % overloadKey)

	def getOverloadKey(self, item):
		if item.overloadKey:
			return item.overloadKey
		maxKey = 0
		for tx in self.items:
			if tx.overloadKey:
				maxKey = max(maxKey, tx.overloadKey)
		for tx in self.items:
			if not tx.overloadKey:
				maxKey += 1
				tx.overloadKey = maxKey
		return item.overloadKey

	def getCountOfName(self, name):
		return reduce(lambda acc, taxon: acc + (1 if taxon.getName() == name else 0), self.items, 0)

	@staticmethod
	def findSuitablePure(qtArguments, functions):
		"""
		qtArguments = список квази-типов для аргументов вызывающего выращения (фактических параметров)
		functions = список таксонов типа TaxonFunc
		result = 
			None - значит не готово
			'NoSuitable' = 'No suitable _method_ found for fname(type, type)'
				
		"""
		if None in qtArguments:
			return None
		nArgs = len(qtArguments)
		# Собрать список функций, которые подходят по количеству параметров, с учетом дефолтных значений
		possibleFuncs = []
		for func in functions:
			params = func.getParamsList()
			if len(params) != nArgs:
				# У функции число параметров должно точно соответствовать количеству аргументов.
				# Дефолтные параметры для перегруженных функций запрещены.
				continue
			qtList = [param.buildQuasiType() for param in params]
			if None in qtList:
				return None
			possibleFuncs.append((func, qtList))
		# Если не подошел ни один вариант
		if len(possibleFuncs) == 0:
			return 'NoSuitable'
		# Теперь нужно проверить соответствие
		matches = []
		for func, qtList in possibleFuncs:
			resList = []
			for i, qtArg in enumerate(qtArguments):
				res, err = QuasiType.matchTaxons(qtList[i], qtArg)
				if err:
					break
				resList.append(res)
			else:
				matches.append((func, resList))
		if len(matches) == 0:
			return 'NoSuitable'
		# Если найдено одно соответствие, то задача выполнена
		if len(matches) == 1:
			return matches[0][0]

		# Если вариантов несколько то сначала пробуем найти точное соответствие
		exacts = []
		for func, matchList in matches:
			for res in matchList:
				if res not in ('exact', 'constExact'):
					break
			else:
				exacts.append(func)
		if len(exacts) == 1:
			# Найден один вариант, точно соответствующий по параметрам
			return exacts[0]

		if len(exacts) > 1:
			# Несколько точно подходящих вариантов
			return 'NoSuitable'

		# Точных соответствий нет. Попробуем найти лучшее соответствие
		weights = {'exact': 10, 'constExact': 10, 'upcast': 1, 'constUpcast': 1}
		priors = []
		for func, matchList in matches:
			weight = 0
			for res in matchList:
				weight += weights[res]
			priors.append((func, weight))
		# Сортировка по весу
		priors.sort(key = lambda pair: pair[1])
		# Если первые два равны по весу, то ошибка
		if priors[0][1] == priors[1][1]:
			return 'NoSuitable'
		return priors[0][0]
