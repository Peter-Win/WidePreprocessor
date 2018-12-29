from core.TaxonBlock import TaxonBlock
from Wpp.WppTaxon import WppTaxon

class WppBlock(TaxonBlock, WppTaxon):
	def readBody(self, context):
		from Wpp.WppVar import WppVar
		from Wpp.WppReturn import WppReturn
		from Wpp.WppExpression import WppExpression

		word = context.getFirstWord()
		if word == 'var':
			return WppVar()
		if word == 'return':
		 	return WppReturn()
		# if word == 'if':
		# 	return TaxonIf(self)
		# if word == 'elif' or word == 'else':
		# 	cmd = self.body[-1] if len(self.body) > 0 else None
		# 	if cmd and cmd.type == 'if' and cmd.canAdd():
		# 		return cmd
		# 	context.throwError('Invalid statement "' + word + '" without "if"')

		# Когда все стандартные инструкции закончились, возможен вариант вычисления выражения
		# Последнее выражение функции воспринимается как return
		return WppExpression.create(context.currentLine.strip(), context)

	def export(self, outContext):
		for item in self.items:
			item.export(outContext)