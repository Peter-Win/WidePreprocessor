from Taxon import Taxon

class TaxonCommonVar(Taxon):
	def getTypeTaxon(self):
		return self.items[0] if len(self.items) >= 1 else None
	def getValueTaxon(self):
		return self.items[1] if len(self.items) >= 2 else None
	def buildQuasiType(self):
		txType = self.getTypeTaxon()
		return txType.buildQuasiType() if txType else None

class TaxonVar(TaxonCommonVar):
	""" Классическая переменная.
	Обычно объявляется в блоке.
	Может быть объявлена в модуле, но только private.
	То есть, экспортировать переменные из модуля нельзя.
	"""
	type = 'var'

class TaxonField(TaxonCommonVar):
	""" Поле - переменная класса """
	type = 'field'
	canBeStatic = True

class TaxonReadonly(TaxonCommonVar):
	""" Поле, доступное только для чтения """
	type = 'readonly'

class TaxonParam(TaxonCommonVar):
	""" Формальный параметр функции """
	type = 'param'
