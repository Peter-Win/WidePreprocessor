from Taxon import Taxon

class TaxonOverload(Taxon):
	type = 'overload'

	def addItem(self, taxon):
		# При включении в ovrtload функция лишается имени. Иначе появляются проблемы при построении пути getPathExt
		# Компенсация имени производится в TaxonFunc.getName()
		taxon.name = ''
		super().addItem(taxon)