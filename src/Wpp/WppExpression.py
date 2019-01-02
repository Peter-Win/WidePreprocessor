from Taxon import Taxon
from Wpp.expr.parseExpr import parseExpr
from Wpp.expr.scanLexems import scanLexems

class WppExpression(Taxon):
	@staticmethod
	def create(string, context):
		lexems = parseExpr(string, context)
		node, pos = scanLexems(lexems, 0, {'end'}, context)
		return node.makeTaxon()

	def readHead(self, context):
		# Фиктивная функция. Не используется, т.к. выражение читается из строки. Но вызов этой функции требуется в readWpp
		pass
