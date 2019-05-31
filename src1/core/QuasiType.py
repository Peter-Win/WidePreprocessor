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

Все таксоны, которые так или иначе связаны с типами, должны иметь функцию calcQuasiType(): QuasiType
А таксоны типов должны иметь функцию @classmethod matchQuasiType(left: QuasiType, right: QuasiType): (string, string)
первая строка exact, constExact, upcast, ...
вторая используется как сообщение об ошибке, если первая строка None
"""

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
		if 'unsigned' in childAttrs:
			result.add('unsigned')
			if 'signed' in result:
				result.remove('signed')
	def update(self, attrs):
		self.attrs = QuasiType.mixAttrs(self.attrs, attrs)

	def getDebugStr(self):
		return self.taxon.getDebugStr()

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
		if not result and not errorMsg:
			errorMsg = 'Cannot convert from "%s:%s" to "%s"' % (right.getDebugStr(), right.type, left.getDebugStr())
		return result, errorMsg
