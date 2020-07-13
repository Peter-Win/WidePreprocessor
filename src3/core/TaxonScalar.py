from core.TaxonType import TaxonType
from core.TaxonExpression import TaxonConst
from core.QuasiType import QuasiType

constMatchesInt = {'int': 'constExact'}
constMatchesFloat = {'float': 'constExact', 'fixed': 'constExact', 'int': 'constUpcast'}
# Целые константы могут быть проверены на диапазон числа с плавающей точкой. Поэтому целая константа для float считается подходящей.
# Тем не менее, целое число кастуется в плавающее. Это может быть использовано при поиске лучшего варианта перегруженной функции.
# Но для переменных иначе. Целые и плавающие переменные не могут присваиваться друг другу без специальных преобразований.

class TaxonScalar(TaxonType):
	""" Скалярные типы данных
	В ядре хранится по одному экземпляру каждого из скалярных типов
	Типы short, int, long, float, double Наиболее соответствуют стандарту языка Java
	short: 16 bit, int: 32 bit, long: 64 bit, float: 32 bit, double: 64 bit
	"""
	type = 'scalar'
	propsList = (
		('bool', {'bool': 'constExact'}, {'bool': 'exact'}, 0, 0),
		('int8', constMatchesInt, {'int8': 'exact'}, -128, 127),
		('short', constMatchesInt, {'short': 'exact', 'int8': 'upcast'}, -32768, 32767),
		('int', constMatchesInt, {'int': 'exact', 'short': 'upcast', 'int8': 'upcast'}, -2147483648, 2147483647),
		('long', constMatchesInt, {'long': 'exact', 'int': 'upcast', 'short': 'upcast', 'int8': 'upcast'}, -9223372036854775808, 9223372036854775807),
		('float', constMatchesFloat, {'float': 'exact'}, -3.4E+38, 3.4E+38),
		('double', constMatchesFloat, {'double': 'exact', 'float': 'upcast'}, -1.7E+308, 1.7E+308),
	)

	def __init__(self, props):
		name, matchConst, matchVar, minVal, maxVal = props
		super().__init__(name)
		self.matchConst = matchConst
		self.matchVar = matchVar
		self.minValue = minVal
		self.maxValue = maxVal

	def getDebugStr(self):
		return self.name

	def buildQuasiType(self):
		return QuasiType(self)

	def exportString(self):
		return self.name

	def matchQuasiType(self, left, right): #TODO: Проверять диаазон констант
		rightTaxon = right.taxon
		if isinstance(rightTaxon, TaxonConst):
			result = self.matchConst.get(rightTaxon.constType)
			if result and rightTaxon.isNumber():
				if rightTaxon.value < 0 and ('unsigned' in left.attrs):
					return None, 'Invalid conversion of negative value "%s" to "%s"' % (rightTaxon.value, left.getDebugStr())
				if rightTaxon.value < self.minValue or rightTaxon.value > self.maxValue:
					return None, 'The value "%s" is outside the range of "%s"' % (rightTaxon.value, left.getDebugStr())
			return result, None
		if isinstance(rightTaxon, TaxonScalar):
			result = self.matchVar.get(right.taxon.name)
			return result, None
		return None, None