from core.TaxonExpression import TaxonConst, TaxonNamed, TaxonCall
from out.lexems import Lex

class TSConst(TaxonConst):

	def exportLexems(self, lexems, style):
		lexems.append((self.toString(style), 'const'))

	def toString(self, style):
		if self.constType == 'string':
			return self.makeString(self.value, style)
		if self.constType == 'null':
			return 'null'
		if self.constType == 'bool':
			return 'true' if self.value else 'false'
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

class TSNamed(TaxonNamed):
	def exportLexems(self, lexems, style):
		target = self.getTarget()
		# TODO: Здесь надо проверять, не является ли уже оно частью конструкции this. А так же static
		if target.type == 'field':
			lexems += [Lex.keyword('this'), Lex.dot]
		lexems.append(Lex.varName(target.getName()))

class TSCall(TaxonCall):
	def exportLexems(self, lexems, style):
		self.getCaller().exportLexems(lexems, style)
		lexems.append(Lex.paramsBegin)
		args = self.getArguments()
		if len(args) > 0:
			for arg in args:
				arg.exportLexems(lexems, style)
				lexems.append(Lex.paramDiv)
			lexems[-1] = Lex.paramDivLast
		lexems.append(Lex.paramsEnd)
		# Данный таксон может быть отдельной строкой кода, если это вызов функции без использования результата
		# В этом случае нужна точка с запятой
		if self.owner.type == 'body':
			lexems.append(Lex.instrDiv)
