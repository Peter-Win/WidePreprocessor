from Taxon import Taxon
from TaxonDictionary import TaxonDictionary
from core.Operators import BinOpNames, UnOpNames
# from core.Signature import Signature

class TaxonOverloads(Taxon):
	type = 'Overloads'

	# def canFind(self, caller):
	# 	return Signature.canCreateFromCall(caller)

	# def find(self, caller):
	# 	sign = Signature.createFromCall(caller)
	# 	weights = []
	# 	for fn in self.items:
	# 		curWeight = sign.match(fn)
	# 		if curWeight:
	# 			weights.append((curWeight, fn))
	# 	if len(weights) == 0:
	# 		self.throwError('Cant match call of '+self.getPath()+' '+str(sign))
	# 	weights.sort()
	# 	if len(weights) > 2 and weights[0][0] == weights[1][0]:
	# 		self.throwError('Too many matches for '+self.getPath()+' '+str(sign))
	# 	return weights[0][1]

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

	def getAutoInits(self):
		""" Список параметров с автоинициализацией """
		return [param for param in self.getParams() if 'init' in param.attrs]

	def checkSignature(self, sign):
		""" Сигнатура создаётся таксоном типа Call. А здесь происходит сопоставление
		Возвращается числовой вес. Чем выше, тем лучше соответствие.
		"""
		pass

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
	def __init__(self, bMethod = False):
		super().__init__()
		self.bMethod = bMethod
	def isMethod(self):
		return self.bMethod
	def clone(self, newCore):
		taxon = super().clone(newCore)
		taxon.bMethod = self.bMethod
		return taxon
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

