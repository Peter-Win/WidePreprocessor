from Taxon import Taxon
from TaxonDictionary import TaxonDictionary
from core.Operators import BinOpNames, UnOpNames
from core.Signature import Signature
from core.QuasiType import QuasiType

class TaxonOverloads(Taxon):
	type = 'Overloads'

	def canFind(self, caller):
		return Signature.canCreateFromCall(caller)

	def find(self, caller):
		sign = Signature.createFromCall(caller)
		weights = []
		for fn in self.items:
			curWeight = sign.match(fn)
			if curWeight:
				weights.append((curWeight, fn))
		if len(weights) == 0:
			self.throwError('Cant match call of '+self.getPath()+' '+str(sign))
		weights.sort()
		if len(weights) > 2 and weights[0][0] == weights[1][0]:
			self.throwError('Too many matches for '+self.getPath()+' '+str(sign))
		return weights[0][1]

	def isReady(self):
		for fn in self.items:
			if not fn.isReady():
				return False
		return True

	def isReadyFull(self):
		for fn in self.items:
			if not fn.isReadyFull():
				return False
		return True
	def getDebugStr(self):
		return self.name

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
		from core.TaxonLocalType import TaxonLocalType
		# Тип результата (если есть) стоит первым в списке
		hasResult = len(self.items) > 1 and isinstance(self.items[1], TaxonLocalType)
		return self.items[1] if hasResult else None

	def buildQuasiType(self):
		resultType = self.getResultType()
		if not resultType:
			return None
		return QuasiType.combine(self, resultType)

	def getParams(self):
		""" Линейный список параметров. А для доступа по имени лучше использовать dictionary """
		start = 2 if self.getResultType() else 1
		return self.items[start:]

	def getAutoInits(self):
		""" Список параметров с автоинициализацией """
		return [param for param in self.getParams() if 'init' in param.attrs]

	def checkSignature(self, sign):
		""" Сигнатура создаётся таксоном типа Call. А здесь происходит сопоставление
		Возвращается числовой вес. Чем выше, тем лучше соответствие.
		"""
		pass

	def isReady(self):
		for param in self.getParams():
			if not param.isReady():
				return False
		resultType = self.getResultType()
		return resultType.isReady() if resultType else True
	def isReadyFull(self):
		for param in self.getParams():
			if not param.isReadyFull():
				return False
		resultType = self.getResultType()
		return resultType.isReadyFull() if resultType else True
	def getDebugStr(self):
		s = '%s %s(%s)' % (self.type, self.name, ', '.join([i.getDebugStr() for i in self.getParams()]))
		resultType = self.getResultType()
		if resultType:
			s += ':'+resultType.getDebugStr()
		return s

class TaxonFunc(TaxonCommonFunc):
	type = 'Func'

class TaxonMethod(TaxonCommonFunc):
	"""
	Attributes: const, static|virtual|override, public|pritected|private
	"""
	type = 'Method'
	canBeStatic = True

class TaxonOperator(TaxonCommonFunc):
	type = 'Operator'
	__slots__ = ('bMethod')
	def __init__(self, bMethod = False):
		super().__init__()
		self.bMethod = bMethod
	def isMethod(self):
		return self.bMethod
	def isBinary(self):
		return len(self.getParams()) == 1
	def isUnary(self):
		return len(self.getParams()) == 0
	def getPossibleName(self):
		""" Альтернативное имя, которое используется для тех языков, которые не поддерживают перегрузку операторов """
		if self.altName:
			return self.altName
		name = (BinOpNames if self.isBinary() else UnOpNames)[self.name]
		if 'right' in self.attrs:
			name = 'r' + name
		return name

class TaxonConstructor(TaxonMethod):
	type = 'Constructor'
	key = '@constructor'
	def __init__(self):
		super().__init__(self.key)

