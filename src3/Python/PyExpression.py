from core.TaxonExpression import TaxonBinOp, TaxonConst, TaxonNamed, TaxonCall, TaxonNew, TaxonMemberAccess, TaxonThis
from out.lexems import Lex
from Python.PyTaxon import PyTaxon
from core.TaxonAltName import TaxonAltName

class PyConst(TaxonConst, PyTaxon):
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

class PyThis(TaxonThis, PyTaxon):
	def exportLexems(self, level, lexems, style):
		lexems.append(Lex.keyword('self'))

class PyNamed(TaxonNamed, PyTaxon):
	def onInit(self):
		from utils.forceThis import forceThis
		forceThis(self)

	def exportLexems(self, level, lexems, style):
		target = self.getTarget()
		lexems.append(Lex.varName(target.getName()))

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
		if 'instruction' in self.attrs:
			self.exportLine(level, lexems, style, line)
		else:
			lexems += line

class PyNew(TaxonNew, PyTaxon):
	def exportLexems(self, level, lexems, style):
		target = self.getCaller().getTarget()
		constr = target.findConstructor()
		newLex = [Lex.className(target.getName())]
		if constr and constr.type == 'overload':
			realConstr = constr.items[self.overloadIndex]
			if realConstr.isStatic():
				newLex += [Lex.dot, Lex.funcName(TaxonAltName.getAltName(realConstr))]
		lexems += newLex
		lexems.append(Lex.bracketBegin)
		args = self.getArguments()
		if len(args):
			for arg in args:
				arg.exportLexems(level, lexems, style)
				lexems.append(Lex.paramDiv)
			lexems[-1] = Lex.paramDivLast
		lexems.append(Lex.bracketEnd)

class PyBinOp(TaxonBinOp, PyTaxon):
	def exportLexems(self, level, lexems, style):
		line = []
		self.getLeft().exportLexemsPrior(line, style)
		line.append(Lex.binop(self.opcode))
		self.getRight().exportLexemsPrior(line, style)
		if 'instruction' in self.attrs:
			self.exportLine(level, lexems, style, line)
		else:
			lexems += line

class PyMemberAccess(TaxonMemberAccess, PyTaxon):
	def exportLexems(self, level, lexems, style):
		self.getLeft().exportLexemsPrior(lexems, style)
		lexems += [Lex.dot, Lex.fieldName(self.memberName)]
