from core.types.TaxonTypeExprName import TaxonTypeExprName
from out.lexems import Lex

class TSTypeExprName(TaxonTypeExprName):
	def exportLexems(self, lexems, style):
		txType = self.getTypeTaxon()
		lexems.append(Lex.typeName(txType.getName()))
