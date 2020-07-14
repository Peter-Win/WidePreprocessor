"""
TypeAlias - специальный таксон, который используется только в ядре.
Вводит синонимы типов с модифицированными атрибутами.
"""
from core.TaxonTypedef import TaxonTypedef

class TaxonTypeAlias(TaxonTypedef):
	def __init__(self, name, aliasName):
		super().__init__(name)
		self.aliasName = aliasName

	def getName(self):
		return self.aliasName