from Taxon import Taxon

class TaxonAltName(Taxon):
	type = 'altName'
	__slots__ = ('altName')

	def __init__(self, name=''):
		super().__init__()
		self.altName = name

	@staticmethod
	def getAltName(taxon):
		for item in taxon.items:
			if item.type == TaxonAltName.type:
				return item.altName

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.altName = src.altName
