from core.TaxonFunc import TaxonFunc, TaxonMethod, TaxonConstructor, TaxonOperator
from out.lexems import Lex
from core.TaxonClass import TaxonClass
from core.TaxonAltName import TaxonAltName
from utils.makeStaticConstructor import makeStaticConstructor

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

def exportMethod(method, lexems, style):
	# access level
	accessLevel = TaxonClass.getAccessLevelFor(method)
	if accessLevel:
		lexems += [Lex.keyword(accessLevel), Lex.space]
	isConstructor = method.type == 'constructor'
	# static
	if method.isStatic():
		lexems += [Lex.keyword('static'), Lex.space]
		isConstructor = False

	if isConstructor:
		lexems.append(Lex.keyword('constructor'))
	else:
		lexems.append(Lex.funcName(method.getName()))
			
	lexems.append(Lex.paramsBegin)
	for param in method.getParamsList():
		param.exportLexems(lexems, style)
		lexems.append(Lex.paramDiv)
	if lexems[-1] == Lex.paramDiv:
		lexems[-1] = Lex.paramDivLast
	lexems.append(Lex.paramsEnd)
	if not isConstructor:
		lexems.append(Lex.colon)
		typeExpr = method.getResultTypeExpr()
		if typeExpr:
			typeExpr.exportLexems(lexems, style)
		else :
			lexems.append(Lex.typeName('void'))
	method.getBody().exportLexems(lexems, style)

class TSMethod(TaxonMethod):
	def exportLexems(self, lexems, style):
		exportMethod(self, lexems, style)

class TSOperator(TaxonOperator):
	def getName(self):
		from core.operators import opcodeMap
		from core.TaxonAltName import TaxonAltName
		name = TaxonAltName.getAltName(self)
		if not name:
			descr = opcodeMap[self.name]
			name = descr[1]
		return name
	def exportLexems(self, lexems, style):
		exportMethod(self, lexems, style)
	def exportBinOp(self, binOp, style):
		lexems = []
		binOp.getLeft().exportLexems(lexems, style)
		lexems += [Lex.dot, Lex.funcName(self.getName()), Lex.bracketBegin]
		binOp.getRight().exportLexems(lexems, style)
		lexems.append(Lex.bracketEnd)
		return lexems


class TSConstructor(TaxonConstructor):
	def isNeedRebuild(self):
		return 'overload' in self.attrs and len(self.getParamsList()) > 0

	def onInit(self):
		if self.isNeedRebuild():
			# Нужно подождать, пока таксоны типа PyNamed выполнят замену field на self.field
			class TaskWait:
				def check(self):
					return True
				def exec(self):
					makeStaticConstructor(self.taxon)
			self.addTask(TaskWait())

	def exportLexems(self, lexems, style):
		exportMethod(self, lexems, style)