from core.TaxonFunc import TaxonFunc, TaxonMethod, TaxonConstructor
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyCommonFunc(PyTaxon):
	def exportLexems(self, level, lexems, style):
		line = [Lex.keyword('def'), Lex.space, Lex.funcName(self.getName()), Lex.paramsBegin]

		paramLexems = []
		isStatic = False
		if self.owner.isClass():
			isStatic = self.isStatic()
			if not isStatic:
				paramLexems.append([Lex.keyword('self')])

		for param in self.getParamsList():
			pdef = []
			param.exportLexems(0, pdef, style)
			paramLexems.append(pdef)

		if len(paramLexems) > 0:
			for pl in paramLexems:
				line += pl
				line.append(Lex.paramDiv)
			line[-1] = Lex.paramDivLast

		line += [Lex.paramsEnd, Lex.colon]
		if isStatic:
			self.exportLine(level, lexems, style, [Lex.keyword('@staticmethod')])
		self.exportLine(level, lexems, style, line)

		self.exportInternalComment(level + 1, lexems, style)
		self.getBody().exportLexems(level + 1, lexems, style)

class PyFunc(TaxonFunc, PyCommonFunc):
	pass

class PyMethod(TaxonMethod, PyCommonFunc):
	pass

class PyConstructor(TaxonConstructor, PyCommonFunc):
	def getName(self):
		return '__init__'