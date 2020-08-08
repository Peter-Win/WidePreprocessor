from core.TaxonFunc import TaxonFunc
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyFunc(TaxonFunc, PyTaxon):
	def exportLexems(self, level, lexems, style):
		line = [Lex.keyword('def'), Lex.space, Lex.funcName(self.getName()), Lex.paramsBegin]
		paramsList = self.getParamsList()
		for i, param in enumerate(paramsList):
			param.exportLexems(level, line, style)
			line.append(Lex.paramDiv if i != len(paramsList) - 1 else Lex.paramDivLast)

		line += [Lex.paramsEnd, Lex.colon]
		self.exportLine(level, lexems, style, line)

		self.exportInternalComment(level + 1, lexems, style)
		self.getBody().exportLexems(level + 1, lexems, style)
