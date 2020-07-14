from core.TaxonModule import TaxonModule
from Wpp.WppTaxon import WppTaxon
from Wpp.readWpp import readWpp

class WppModule(TaxonModule, WppTaxon):
	validSubTaxons = ('typedef', 'var')
	
	def read(self, context):
		readWpp(context, self)

	def findUp(self, name):
		# При поиске вверх нужно искать все таксоны модуля
		result = self.findItem(name)
		if result:
			return result
		return super().findUp(name)

	def export(self, outContext):
		writeContext = outContext.createFile(self.name + self.extension)
		# self.exportComment(outContext)
		# if self.importBlock:
		# 	self.importBlock.export(writeContext)

		for item in self.items:
			item.export(writeContext)
			# Между компонентами модуля вставляется пустая строка
			writeContext.eol()
		writeContext.close()
