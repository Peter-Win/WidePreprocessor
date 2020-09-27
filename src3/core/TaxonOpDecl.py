"""
Базовые деклараторы операторов.
Хранятся в ядре.

В разных языках есть специфические реализации для разных операторов.
Примеры:
- Логические операторы в Python: or, and, not
- Сравнение в PHP, JavaScript, TypeScript: ===, !==
- В Java и C++ нет возведения в степень
- В Java, JS, TS оператор сдвига вправо для беззнаковых значений: >>>
- Целочисленное деление в Python: //
Эти различия закладываются в декларацию операторов для каждого языка.
Поэтому каждый таксон бинарного оператора содержит ссылку на декларацию.

"""
from Taxon import Taxon
from core.QuasiType import QuasiType

class TaxonDeclAssignBase(Taxon):
	""" Базовый оператор присваивания """
	type = 'declAssignBase'
	def getOpcode(self):
		return '='

	def exportBinOp(self, binop):
		return '%s = %s' % (binop.getLeft().exportString(), binop.getRight().exportString())

class TaxonDeclBinOp(Taxon):
	type = 'declBinOp'
	def __init__(self, originalOpcode, modifiedOpcode, leftType, rightType, resultType):
		""" Имя таксона включает исходный код операции, чтобы в любом ядре имена совпадали
		Иначе не получится клонировать, т.к. там сопоставляется имя
		"""
		super().__init__('%s %s, %s' % (originalOpcode, leftType.getDebugStr(), rightType.getDebugStr()))
		self.opcode = modifiedOpcode
		self.leftType = leftType
		self.rightType = rightType
		self.resultType = resultType

	def getOpcode(self):
		return self.opcode

	def buildQuasiType(self, binop):
		return self.resultType.buildQuasiType()

	def matchTypes(self, leftQt, rightQt):
		leftRes, leftErr = QuasiType.matchTaxons(self.leftType, leftQt)
		rightRes, rightErr = QuasiType.matchTaxons(self.rightType, rightQt)
		return leftRes, rightRes
