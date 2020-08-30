from core.TaxonClass import TaxonClass
from Wpp.WppTaxon import WppTaxon
from utils.nameCheck import checkUpperCamelCase
from Wpp.WppFuncHelper import WppFuncHelper

class WppClass(TaxonClass, WppTaxon):
	validSubTaxons = ('field', 'method', 'constructor')

	def checkName(self, name):
		return checkUpperCamelCase(name, self.type)

	def checkDup(self, taxon, dup, context):
		if WppFuncHelper.checkDup(taxon, dup, context):
			return
		super().checkDup(taxon, dup, context)

	def findUp(self, name, caller):
		# При поиске вверх нужно искать все таксоны класса
		result = self.findItem(name)
		if result:
			return result
		return super().findUp(name, caller)

	def readHead(self, context):
		words = context.currentLine.split()
		if len(words) < 2:
			context.throwError('Required class name')
		self.name = words[-1]
		self.attrs = set(words[1:-1])

	def addTaxon(self, taxon, context):
		res = WppFuncHelper.addTaxon(self, taxon, context)
		if res:
			return res
		return super().addTaxon(taxon, context)

	def export(self, outContext):
		# Сначала экспорт заголовка класса
		parts = [self.type] + self.getExportAttrs() + [self.getName()]
		head = ' '.join(parts)
		outContext.writeln(head)
		with outContext:
			for taxon in self.items:
				# Некоторые таксоны не умеют себя экспортить. Им надо помочь. Но большинство умеет.
				taxon.export(outContext)
