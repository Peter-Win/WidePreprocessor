from core.TaxonBlock import TaxonBlock
from Wpp.WppTaxon import WppTaxon

class WppBlock(TaxonBlock, WppTaxon):
	def readBody(self, context):
		from Wpp.WppVar import WppVar
		from Wpp.WppReturn import WppReturn
		from Wpp.WppExpression import WppExpression
		from Wpp.WppIf import WppIf
		from Wpp.WppForeach import WppForeach

		word = context.getFirstWord()
		if word == 'var':
			return WppVar()
		if word == 'return':
			return WppReturn()
		if word == 'if':
			return WppIf()
		if word == 'elif' or word == 'else':
			cmd = self.items[-1] if self.items else None
			if cmd and cmd.type == 'If' and cmd.canAdd():
				return cmd
			context.throwError('Invalid statement "' + word + '" without "if"')
		if word == 'foreach':
			return WppForeach()

		# Когда все стандартные инструкции закончились, возможен вариант вычисления выражения
		# Последнее выражение функции воспринимается как return
		return WppExpression.create(context.currentLine.strip(), context)

	def addTaxon(self, taxon):
		if taxon not in self.items:
			self.addItem(taxon)
		return taxon

	def export(self, outContext):
		for item in self.items:
			item.export(outContext)

	def tryAutoReturn(self, funcType):
		""" Возможная автозамена последнего выражения на return """
		from Wpp.WppReturn import WppReturn
		from core.TaxonExpression import TaxonExpression
		bodyItems = self.items
		if funcType and len(bodyItems) > 0:
			lastCmd = bodyItems[-1]
			if isinstance(lastCmd, TaxonExpression):
				#TODO: Здесь надо проверять соответствие типов
				bodyItems.pop()
				self.addItem(WppReturn.createAuto(lastCmd))
