from core.TaxonExpression import TaxonConst, TaxonNamed
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
		lexems.append(Lex.varName(self.getTarget().getName()))