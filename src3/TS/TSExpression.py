from core.TaxonExpression import TaxonConst, TaxonNamed, TaxonCall, TaxonNew, TaxonMemberAccess, TaxonBinOp, TaxonThis, TaxonSuper
from out.lexems import Lex
from TS.exportLexemsPrior import exportLexemsPrior

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
	def onInit(self):
		# Выполнить подстановку this к неявно вызываемым членам класса
		from utils.forceThis import forceThis
		forceThis(self)
	def exportLexems(self, lexems, style):
		target = self.getTarget()
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
		if 'instruction' in self.attrs:
			lexems.append(Lex.instrDiv)

class TSNew(TaxonNew):
	def exportLexems(self, lexems, style):
		target = self.getCaller().getTarget()
		lexTargetName = Lex.className(target.getName())
		bNew = True
		if self.overloadKey:
			# Static constructor
			conOver = target.findConstructor()
			realConstr = conOver.getImplementationByKey(self.overloadKey)
			if realConstr.isStatic():
				lexems += [lexTargetName, Lex.dot, Lex.funcName(realConstr.getName())]
				bNew = False
		if bNew:
			lexems += [Lex.keyword('new'), Lex.space, lexTargetName]
		lexems.append(Lex.paramsBegin)
		args = self.getArguments()
		if len(args) > 0:
			for arg in args:
				arg.exportLexems(lexems, style)
				lexems.append(Lex.paramDiv)
			lexems[-1] = Lex.paramDivLast
		lexems.append(Lex.paramsEnd)

class TSMemberAccess(TaxonMemberAccess):
	def exportLexems(self, lexems, style):
		self.getLeft().exportLexems(lexems, style)
		lexems += [Lex.dot, Lex.fieldName(self.memberName)]

class TSBinOp(TaxonBinOp):
	def exportLexems(self, lexems, style):
		from TS.TSOpDecl import TSDeclBinOp
		decl = self.getDeclaration()
		line = decl.exportBinOp(self, style) if decl else TSDeclBinOp.export(self, style)
		lexems += line
		if 'instruction' in self.attrs:
			lexems.append(Lex.instrDiv)

class TSThis(TaxonThis):
	def exportLexems(self, lexems, rules):
		lexems.append(Lex.keyword('this'))

class TSSuper(TaxonSuper):
	def exportLexems(self, lexems, rules):
		if self.isConstructor():
			lexems.append(Lex.keyword('super'))
		elif self.isOverride():
			lexems += [Lex.keyword('super'), Lex.dot, Lex.funcName(self.getTarget().getName())]
