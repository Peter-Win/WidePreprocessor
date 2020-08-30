"""
Квази-тип используется для проверки соответствия типов.
Это происходит при инициализации переменных. Например:
var count: unsigned int = 22  - Это правильно.
field private name: String = 22 - Это неправильно.
Другой случай - поиск подходящей сигнатуры в списке перегрузок. Там нужно оценить, что лучше подходит
Например
для fn(1, 2)
В принципе подходят fn(int, int) и fn(float, float). Но первый вариант подходит лучше.

Базовый квази-тип включает атрибуты и таксон типа или константы.
В некоторых случаях могут добавиться дополнительные данные.
Например, массив может содержать тип элемента. А ассоциативный массив - типы ключа и значения.
Тип массива знает о своих специфичных данных и использует их для проверок. Остальным типам эти данные не нужны.

Все таксоны, которые так или иначе связаны с типами, должны иметь функцию buildQuasiType(): QuasiType
А таксоны типов должны иметь функцию @classmethod matchQuasiType(left: QuasiType, right: QuasiType): (string, string)
первая строка exact, constExact, upcast, ...
вторая используется как сообщение об ошибке, если первая строка None
"""
from Taxon import Taxon

class QuasiType:
	def __init__(self, taxon, attrs = None):
		self.type = taxon.type
		self.taxon = taxon
		self.attrs = QuasiType.mixAttrs(taxon.attrs, attrs)

	def isType(self, typeName):
		return self.taxon.type == typeName

	def buildQuasiType(self):
		return self

	@staticmethod
	def mixAttrs(parentAttrs, childAttrs):
		if not childAttrs:
			return parentAttrs
		result = parentAttrs.copy()
		for childA in childAttrs:
			if 'unsigned' == childA:
				result.add('unsigned')
				if 'signed' in result:
					result.remove('signed')
			else:
				result.add(childA)
		return result
	def update(self, attrs):
		self.attrs = QuasiType.mixAttrs(self.attrs, attrs)

	def getDebugStr(self):
		attrsStr = Taxon.AttrsToStr([a for a in self.attrs if a not in {'public'}])
		if attrsStr:
			attrsStr += ' '
		return attrsStr + self.taxon.getDebugStr()

	def showType(self):
		if self.taxon.type == 'const':
			return self.taxon.constType
		return self.taxon.exportString()

	def exportString(self):
		return self.taxon.exportString()

	@staticmethod
	def combine(owner, slave):
		quasiInfo = slave.buildQuasiType()
		quasiInfo.update(owner.attrs)
		return quasiInfo

	@staticmethod
	def matchTaxons(left, right):
		""" left = right
		left, right: Taxon
		Проверить, возможно ли присваивание
		Возвращает пару строк: (exact | upcast | constExact | constUpcast, errorMessage)
		"""
		leftType = left.buildQuasiType()
		rightType = right.buildQuasiType()
		result, errorMsg = leftType.taxon.matchQuasiType(leftType, rightType)
		if not result and not errorMsg and hasattr(rightType.taxon, 'matchQuasiTypeReverse'):
			result, errorMsg = rightType.taxon.matchQuasiTypeReverse(leftType, rightType)
		if not result and not errorMsg:
			rightSource = right.inst if hasattr(right, 'inst') else right
			rightStr = rightSource.exportString() if hasattr(rightSource, 'exportString') else rightSource.getDebugStr()
			# errorMsg = 'Cannot convert from "%s:%s" to "%s"' % (rightStr, rightType.showType(), left.exportString())
			errorMsg = 'Cannot convert from "%s" to "%s"' % (rightType.getDebugStr(), left.exportString())
		return result, errorMsg
