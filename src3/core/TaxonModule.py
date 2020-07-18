from TaxonDict import TaxonDict

class TaxonModule(TaxonDict):
	type = 'module'

	def isModule(self):
		return True

	def findUp(self, name, caller):
		# При поиске вверх нужно искать все таксоны модуля
		result = self.findItem(name)
		if result:
			return result
		return super().findUp(name, caller)

