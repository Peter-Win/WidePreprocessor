from core.TaxonModule import TaxonModule
from Wpp.WppTaxon import WppTaxon
from Wpp.readWpp import readWpp
from core.TaxonComment import TaxonComment

class WppModule(TaxonModule, WppTaxon):
	validSubTaxons = ('typedef', 'var', 'func')
	
	def read(self, context):
		readWpp(context, self)

	def export(self, outContext):
		writeContext = outContext.createFile(self.name + self.extension)
		prevTaxon = None
		for item in self.items:
			item.export(writeContext)
			# Между компонентами модуля вставляется пустая строка
			if prevTaxon and prevTaxon.type != TaxonComment.type:
				writeContext.eol()
			prevTaxon = item
		writeContext.close()
