from core.TaxonExpression import TaxonConst, TaxonNamed, TaxonCall
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyConst(TaxonConst):
	def exportLexems(self, level, lexems, style):
		lexems.append((self.toString(style), 'const'))

	def toString(self, style):
		if self.constType == 'string':
			return self.makeString(self.value, style)
		if self.constType == 'null':
			return 'None'
		if self.constType == 'bool':
			return 'True' if self.value else 'False'
		if self.constType in ('int', 'fixed'):
			return str(self.value)
		if self.constType == 'float':
			return self.srcValue if self.srcValue else str(self.value)
		self.throwError('Invalid const type %s' % self.constType)

	@staticmethod
	def makeString(value, style):
		single = style.get('singleQuote')
		if single:
			quote = "'"
		else:
			quote = '"'
		value = value.replace(quote, "\\" + quote)
		value = value.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
		return quote + value + quote

class PyNamed(TaxonNamed):
	def exportLexems(self, level, lexems, style):
		lexems.append(Lex.varName(self.getTarget().getName()))

class PyCall(TaxonCall, PyTaxon):
	def exportLexems(self, level, lexems, style):
		line = []
		self.getCaller().exportLexems(0, line, style)
		line.append(Lex.paramsBegin)
		args = self.getArguments()
		if len(args) > 0:
			for arg in args:
				arg.exportLexems(0, line, style)
				line.append(Lex.paramDiv)
			line[-1] = Lex.paramDivLast
		line.append(Lex.paramsEnd)
		# Данный таксон может быть отдельной строкой кода, если это вызов функции без использования результата
		# В этом случае нужна точка с запятой
		if self.owner.type == 'body':
			self.exportLine(level, lexems, style, line)
		else:
			lexems += line
