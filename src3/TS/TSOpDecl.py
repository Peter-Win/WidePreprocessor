from core.TaxonOpDecl import TaxonDeclBinOp, TaxonDeclAssignBase
from TS.exportLexemsPrior import exportLexemsPrior
from out.lexems import Lex

class TSDeclBinOp(TaxonDeclBinOp):
	def exportBinOp(self, binOp, style):
		return TSDeclBinOp.export(binOp, style)

	@staticmethod
	def export(binOp, style):
		line = []
		exportLexemsPrior(binOp.getLeft(), line, style)
		line.append(Lex.binop(binOp.getOpcode()))
		exportLexemsPrior(binOp.getRight(), line, style)
		return line

class TSDeclAssignBase(TaxonDeclAssignBase):
	def exportBinOp(self, binOp, style):
		line = []
		exportLexemsPrior(binOp.getLeft(), line, style)
		line.append(Lex.binop('='))
		exportLexemsPrior(binOp.getRight(), line, style)
		return line
