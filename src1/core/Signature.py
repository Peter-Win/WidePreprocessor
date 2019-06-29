from core.QuasiType import QuasiType

class Signature:
	"""
	Сигнатура нужна для поиска функции среди перегруженных по типу параметров.
	Операция вызова функции может сформировать список фактических параметров.
	Среди них могут быть обращения к параметрам и переменным, у которых известен тип.
	Так же могут быть константы. true|false и строки имеют точный тип.
	А вот числа могут приводиться к разным типам. Н.р. 1 -> int, unsigned int, float, double.
	Null подходит к разным классам, но не годится для скалярных типов и строк.
	В ряде случаев известен тип результата, но так же возможен случай, когда результат не известен.
	"""
	def __init__(self):
		self.params = []	# Квази-типы

	@staticmethod
	def createFromCall(callTaxon):
		""" Создать сигнатуру из таксона типа Call """
		inst = Signature()
		for param in callTaxon.getArguments():
			inst.params.append(param.buildQuasiType())
		return inst

	@staticmethod
	def canCreateFromCall(callTaxon):
		return callTaxon.isReadyFull()

	def __str__(self):
		return '; '.join([p.exportString() for p in self.params])

	def match(self, funcTaxon):
		"""
		Сопоставить сигнатуру с объявлением функции (Func, Method, Constructor, ...)
		Возвращается числовой вес
		"""
		formalParamsList = funcTaxon.getParams()
		if len(self.params) > len(formalParamsList):
			# Если список параметров сигнатуры длиннее, чем список формальных параметров, значит нет соответствия
			return 0
		# Специальный случай - функция без параметров
		if len(formalParamsList) == 0:
			return 1
		sum = 0
		for i, formalParam in enumerate(formalParamsList):
			if i < len(self.params):
				# Если параметр сигнатуры соответствует формальному параметру функции, то требуется проверить соответствие типов
				matchResult, errMessage = QuasiType.matchTaxons(formalParam, self.params[i])
			else:
				# Нужно проверить наличие значение параметра по-умолчанию.
				val = formalParam.getValueTaxon()
				# Если его нет, то сигнатура не соответствует функции
				matchResult = 'default' if val else ''
			if not matchResult:
				return 0
			sum += weights[matchResult]
		return sum

weights = {
	'exact': 3,
	'constExact': 3,
	'default': 2,
	'upcast': 1,
	'constUpcast': 1,
}
