from TaxonDictionary import TaxonDictionary
from core.QuasiType import QuasiType

class TaxonArray(TaxonDictionary):
	type = 'Array'

	def matchQuasiType(self, left, right): #TODO: Проверять unsigned и диаазон констант
		if left.taxon.type != 'Array':
			self.throwError('Required Array instead of ' + left.taxon.type)
		qtItem = left.itemType.buildQuasiType()
		if right.taxon.type == 'ArrayValue':
			# Необходимо проверить каждый элемент значения [a, b, c], соответствует ли он типу элементов массива
			for srcItemTaxon in right.taxon.items:
				code, errMsg = qtItem.matchTaxons(qtItem, srcItemTaxon)
				if errMsg:
					self.throwError(errMsg)
			# Будем считать, что массив соответствует типу, даже если элементы имеют другие коды, н.р. constUpcast
			return 'constExact', None
		if right.taxon.type == 'Array':
			# Нужно проверить соответствие типов элементов
			return QuasiType.matchTaxons(left.itemType, right.itemType)
		return None, None
