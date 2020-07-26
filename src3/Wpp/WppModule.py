from core.TaxonModule import TaxonModule
from Wpp.WppTaxon import WppTaxon
from Wpp.readWpp import readWpp
from core.TaxonComment import TaxonComment
from utils.nameCheck import checkLowerCamelCase
from Wpp.WppFuncHelper import WppFuncHelper

class WppModule(TaxonModule, WppTaxon):
	validSubTaxons = ('typedef', 'var', 'func')
	__slots__ = ('altNames')
	def __init__(self, name=''):
		super().__init__(name)
		self.altNames = {}
	
	def checkName(self, name):
		return checkLowerCamelCase(name, self.type)

	def checkDup(self, taxon, dup, context):
		WppFuncHelper.checkDup(taxon, dup, context)
		super().checkDup(taxon, dup, context)

	def read(self, context):
		readWpp(context, self)

	def addTaxon(self, taxon, context):
		res = WppFuncHelper.addTaxon(self, taxon, context)
		if res:
			return res
		return super().addTaxon(taxon, context)

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
