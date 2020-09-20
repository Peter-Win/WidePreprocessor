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

	def exportBinOp(self, binop):
		return '%s = %s' % (binop.getLeft().exportString(), binop.getRight().exportString())

def priorExport(subTaxon):
	result = subTaxon.exportString()
	if subTaxon.isNeedBrackets():
		result = '(%s)' % result
	return result


class TaxonDeclBinOp(Taxon):
	type = 'declBinOp'
	def __init__(self, opcode, leftType, rightType, resultType):
		super().__init__('%s %s, %s' % (opcode, leftType.exportString(), rightType.exportString()))
		self.leftType = leftType
		self.rightType = rightType
		self.resultType = resultType

	def buildQuasiType(self, binop):
		return self.resultType.buildQuasiType()

	def exportBinOp(self, binop):
		return '%s %s %s' % (priorExport(binop.getLeft()), binop.opcode, priorExport(binop.getRight()))

	def matchTypes(self, leftQt, rightQt):
		leftRes, leftErr = QuasiType.matchTaxons(self.leftType, leftQt)
		rightRes, rightErr = QuasiType.matchTaxons(self.rightType, rightQt)
		return leftRes, rightRes
