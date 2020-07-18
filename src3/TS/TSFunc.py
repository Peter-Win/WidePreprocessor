from core.TaxonFunc import TaxonFunc
from out.lexems import Lex

class TSFunc(TaxonFunc):
	def exportLexems(self, lexems, style):
		# TODO: сформировать JSDoc
		# export, if public module member
		if self.owner.isModule() and 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		# const funcName = (
		lexems += [Lex.keyword('const'), Lex.space, Lex.funcName(self.getName()), Lex.binop('='), Lex.paramsBegin]

		for param in self.getParamsList():
			param.exportLexems(lexems, style)
			lexems.append(Lex.paramDiv)
		if lexems[-1] == Lex.paramDiv:
			lexems[-1] = Lex.paramDivLast
		# ): {void | resultType} =>
		lexems += [Lex.paramsEnd, Lex.colon]
		typeExpr = self.getResultTypeExpr()
		if typeExpr:
			typeExpr.exportLexems(lexems, style)
		else:
			lexems.append(Lex.typeName('void'))
		lexems.append(Lex.binop('=>'))

		self.getBody().exportLexems(lexems, style)
		lexems.append(Lex.instrDiv)
