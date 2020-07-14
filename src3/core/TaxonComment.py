from Taxon import Taxon

class TaxonComment(Taxon):
	type = "comment"
	def __init__(self, text=''):
		super().__init__()
		self.text = text

	def copyFieldsFrom(self, src):
		super().copyFieldsFrom(src)
		self.text = src.text

	@staticmethod
	def getComments(ownerTaxon):
		return [item.text for item in ownerTaxon.items if item.type == TaxonComment.type]
