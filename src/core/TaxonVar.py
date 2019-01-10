from Taxon import Taxon

class TaxonCommonVar(Taxon):
	def getLocalType(self):
		return self.items[0]

	def getValueTaxon(self):
		return self.items[1] if len(self.items) > 1 else None

	def getFieldDeclaration(self, name):
		return self.getLocalType().getFieldDeclaration(name)

class TaxonVar(TaxonCommonVar):
	""" Классическая переменная.
	Обычно объявляется в блоке.
	Может быть объявлена в модуле, но только private.
	То есть, экспортировать переменные из модуля нельзя.
	"""
	type = 'Var'

class TaxonField(TaxonCommonVar):
	""" Поле - переменная класса """
	type = 'Field'
	canBeStatic = True

class TaxonReadonly(TaxonCommonVar):
	""" Поле, доступное только для чтения """
	type = 'Readonly'

class TaxonParam(TaxonCommonVar):
	""" Формальный параметр функции """
	type = 'Param'
