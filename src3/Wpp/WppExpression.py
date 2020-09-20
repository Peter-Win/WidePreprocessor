from core.TaxonExpression import TaxonCall, TaxonConst, TaxonMemberAccess, TaxonNamed, TaxonNew, TaxonThis, TaxonBinOp, TaxonSuper
from core.TaxonRef import TaxonRef
from Wpp.parser.parseLexems import parseLexems
from Wpp.parser.buildNodes import buildNodes
from core.QuasiType import QuasiType
from core.TaxonOverload import TaxonOverload
from utils.drawTaxonTree import drawTaxonTree
from Wpp.WppClassHelper import checkMemberAccess
from core.TaxonClass import TaxonClass

class WppExpression:
	@staticmethod
	def parse(expression, context):
		lexems = parseLexems(expression, context)
		lexems.append(('END','cmd'))
		node, pos = buildNodes(lexems, 0, {'END'}, context)
		return node.createTaxon(context)


	def priorExportString(self, expr):
		s = expr.exportString()
		if self.prior < expr.prior:
			s = '(' + s + ')'
		return s

class WppConst(TaxonConst, WppExpression):
	@staticmethod
	def create(rawValue):
		if rawValue == 'true':
			return WppConst('bool', True, rawValue)
		if rawValue == 'false':
			return WppConst('bool', False, rawValue)
		if rawValue == 'null':
			return WppConst('null', None, rawValue)
		try:
			intValue = int(rawValue)
			return WppConst('int', intValue, rawValue)
		except:
			pass
		try:
			floatValue = float(rawValue)
			# Здесь нужно отличить float от fixed, тк от этого зависит обратный экспорт в строку в разных языках
			numType = 'float' if 'e' in rawValue or 'E' in rawValue else 'fixed'
			return WppConst(numType, floatValue, rawValue)
		except:
			return WppConst('string', rawValue, rawValue)

	def exportString(self):
		return self.srcValue

class WppThis(TaxonThis, WppExpression):
	def exportString(self):
		return 'this'
	def onInit(self):
		# Здесь не нужно ничего ждать. Достаточно найти класс-владелец
		from core.TaxonClass import TaxonClass
		target = self.findOwnerByTypeEx(TaxonClass)
		if not target:
			self.throwError('Owner class not found for "this" expression');
		self.setTarget(target)

class WppNamed(TaxonNamed, WppExpression):
	def exportString(self):
		return self.targetName

	def onInit(self):
		class TaskBindTarget:
			def check(self):
				return self.taxon.isCanFindUp()
			def exec(self):
				target = self.taxon.startFindUp(self.taxon.targetName)
				if not target:
					self.taxon.throwError('Not found "%s"' % (self.taxon.targetName))
				self.taxon.setTarget(target)
				if target.type in {'field', 'method'}:
					checkMemberAccess(self.taxon, target)
		self.addTask(TaskBindTarget())

class WppMemberAccess(TaxonMemberAccess, WppExpression):
	def onInit(self):
		class TaskCheckAccess:
			def check(self):
				self.member = self.taxon.getTarget()
				return self.member
			def exec(self):
				TaxonClass.checkAccess(self.taxon, self.member)
		self.addTask(TaskCheckAccess())
	def exportString(self):
		return '%s.%s' % (self.getLeft().exportString(), self.memberName)

def checkAgrs(funcName, params, args):
	nArgs = len(args)
	nParams = len(params)
	if nArgs > nParams:
		return '%s takes %d argument but %d were given' % (funcName, nParams, nArgs)
	if nArgs < nParams and not params[nArgs].getValueTaxon():
		return  '%s missing required argument: "%s"' % (funcName, params[nArgs].getName())
	for i, arg in enumerate(args):
		result, errorMsg = QuasiType.matchTaxons(params[i], arg)
		if errorMsg:
			return errorMsg
	return ''

class WppNew(TaxonNew, WppExpression):
	def exportString(self):
		s = self.getCaller().getTarget().name
		s += '(' + ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s

	@staticmethod
	def replaceExt(callTaxon, target, args):
		owner = callTaxon.owner
		owner.items.remove(callTaxon)
		newTaxon = owner.addItem(WppNew())
		newTaxon._location = callTaxon._location
		newTaxon.addItem(TaxonRef.fromTaxon(target))
		for arg in args:
			newTaxon.addItem(arg)
		# Нужно найти конструктор, соответствующий списку аргументов
		con = target.findConstructor()
		if not con and len(args) == 0:
			# Конструктора нет и список аргументов пуст
			return
		if con.type == 'constructor':
			msg = checkAgrs('Constructor', con.getParamsList(), args)
			if msg:
				newTaxon.throwError(msg)
			return
		if con.type == 'overload':
			suitable = TaxonOverload.findSuitablePure(args, con.items)
			if not suitable:
				newTaxon.throwError('Overloaded constructor is not ready');
			if suitable == 'NoSuitable':
				# Здесь возможен специальный случвй - все поля имеют дефолтные значения и используется неявный конструктор без праметров
				# Но будем считать, что в случае переопределения конструктора нужно явно определить конструктор без параметров
				# if len(args) == 0 and target.isAllFieldsInit():
				# 	return
				newTaxon.throwError('No suitable constructor found for %s(%s)' % (target.name, ', '.join(
					[a.buildQuasiType().getDebugStr() for a in args])));
			newTaxon.overloadKey = con.getOverloadKey(suitable)
			return
		tlist = ', '.join([t.buildQuasiType().exportString() for t in args])
		newTaxon.throwError('No suitable constructor found for class %s with arguments (%s)' % (target.getName(), tlist));

class WppSuper(TaxonSuper, WppExpression):
	""" Использование super в WPP отличается от других языков.
	Есть только два случая, где его можно использовать:
	1. В конструкторе. Здесь super используется так же, как в Java или TypeScript.
	2. В виртуальной функции для вызова точно такой же функции базового класса. Причем, имя функции не указывается.
	Python                            TypeScript                             WPP
	def myMethod(self, context):        myMethod(context: Context): void {   method myMethod
		super().onInit(context)             super.onInit(context)                param context: Context
		                                                                         super(context)
	"""
	def exportString(self):
		return 'super'
	def onInit(self):
		from core.TaxonFunc import TaxonFunc
		superType = ''
		ownerFunc = self.findOwnerByTypeEx(TaxonFunc)
		if ownerFunc:
			if ownerFunc.type == 'constructor':
				superType = ownerFunc.type
			elif ownerFunc.type == 'method' and 'override' in ownerFunc.attrs:
				superType = 'override'
		if not superType:
			self.throwError('Super calls are not permitted outside constructors or overrided methods')
		self.attrs.add(superType)
		ownerClass = ownerFunc.findOwnerByTypeEx(TaxonClass)
		if not ownerClass:
			# Вообще такого быть не должно, но на всякий случай проверяем
			self.throwError('Owner class not found for %s' % ownerFunc.getName())
		ext = ownerClass.getExtends()
		if not ext:
			self.throwError('"super" can only be referenced in a derived class')

		if self.isOverride():
			funcName = ownerFunc.name
			class TaskFindFunc:
				def check(self):
					return ownerClass.buildQuasiType()
				def exec(self):
					parent = ext.getParent();
					target = parent.findMember(funcName)
					if not target:
						self.taxon.throwError('Method "%s" does not exist on %s "%s"' % (funcName, parent.type, parent.getName()))
					self.taxon.setTarget(target)
			self.addTask(TaskFindFunc())
		else:
			class TaskFindConstructor:
				def __init__(self, ext):
					self.ext = ext
				def check(self):
					return self.ext.isReady()
				def exec(self):
					parent = self.ext.getParent()
					parentCon = parent.findConstructor()
					if parentCon:
						self.taxon.setTarget(parentCon)
						return
					ext = parent.getExtends()
					if ext:
						self.taxon.addTask(TaskFindConstructor(ext))
					else:
						# Обращение к неявному конструктору без параметров
						self.taxon.throwError('Hidden constructor')
			self.addTask(TaskFindConstructor(ext))

class WppBinOp(TaxonBinOp, WppExpression):
	def readHead(self, context):
		""" Бинарный оператор может использоваться, как самостоятельный элемент тела функции
		Например: this.x = x0
		Но делать здесь ничего не нужно, т.к. выражение уже создано в WppBody.readBody
		"""
		pass

	def exportString(self):
		return self.getDeclaration().exportBinOp(self)

	def export(self, context):
		""" Вариант, когда оператор используется как отдельная инструкция, н.р a = b + 1 """
		context.writeln(self.exportString())

	def onInit(self):
		# Необходимо найти декларацию оператора
		class TaskFindDecl:
			def __init__(self):
				self.leftQType = None
				self.righQType = None
			def check(self):
				if not self.leftQType:
					self.leftQType = self.taxon.getLeft().buildQuasiType()
				if not self.righQType:
					self.righQType = self.taxon.getRight().buildQuasiType()
				return self.leftQType and self.righQType
			def exec(self):
				taxon = self.taxon
				decl, errMsg = taxon.core.findBinOp(taxon.opcode, self.leftQType, self.righQType)
				if errMsg:
					taxon.throwError(errMsg)
				if not decl:
					taxon.throwError('Infalid binop "%s"' % taxon.opcode)
				taxon.addItem(TaxonRef.fromTaxon(decl))
		self.addTask(TaskFindDecl())

class WppCall(TaxonCall, WppExpression):
	__slots__ = ('quasiType')
	def __init__(self):
		super().__init__()
		self.quasiType = None

	def exportString(self):
		s = self.priorExportString(self.getCaller())
		s += '(' + ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s

	def readHead(self, context):
		""" Вызов функции из кода блока без использования возвращаемого результата """
		return
		exprCode = context.currentLine.strip()
		expr = WppExpression.parse(exprCode, context)
		# drawTaxonTree(expr)
		# Скопировать подчиненные элементы из созданного выражения к себе
		for item in expr.items:
			self.addItem(item)

	def export(self, outContext):
		outContext.writeln(self.exportString())

	def buildQuasiType(self):
		return self.quasiType

	def onInit(self):
		class TaskCallerType:
			def __init__(self, caller, args):
				self.caller = caller
				self.args = args
				self.argTypes = list(map(lambda t: None, args))
				self.callerTarget = None
				self.suitable = None
				self.callerQT = None

			def check(self):
				# Сначала нужно дождаться типов всех аргументов
				for i, arg in enumerate(self.args):
					if not self.argTypes[i]:
						self.argTypes[i] = arg.buildQuasiType()
				if not self.callerTarget:
					self.callerTarget = self.caller.getTarget()
				# Обязательное условие: определен тип вызывающего таксона и квази-типы всех аргументов
				if not self.callerTarget or None in self.argTypes:
					return False
				if self.callerTarget.type == TaxonOverload.type:
					self.suitable = TaxonOverload.findSuitablePure(self.args, self.callerTarget.items)
					if not self.suitable:
						return False # Если вернет None, то ждать дальше
					if isinstance(self.suitable, str):
						return True 	# Сообщение об ошибке передать в exec
					self.callerQT = self.suitable.buildQuasiType()
				else:
					# Если вызывающий таксон не ссылается на перегрузку, то надо подождать квази-тип для декларации функции
					if not self.callerQT:
						self.callerQT = self.callerTarget.buildQuasiType()
				return self.callerQT != None

			def exec(self):
				target = self.callerTarget
				if target.type == TaxonOverload.type:
					if self.suitable == 'NoSuitable':
						args = ', '.join([arg.buildQuasiType().exportString() for arg in self.args])
						self.taxon.throwError('No suitable %s found for %s(%s)' % (target.items[0].type, target.getName(), args))
					# Поменять вызывающий таксон
					newCaller = WppNamed(self.suitable.getName())
					newCaller.setTarget(self.suitable)
					self.taxon.changeCaller(newCaller)
				elif target.type == 'class':
					WppNew.replaceExt(self.taxon, target, self.args)
				else:
					formalParams = target.getParamsList()
					errMsg = checkAgrs('%s()' % target.getName(), formalParams, self.args)
					if errMsg:
						self.taxon.throwError(errMsg)
				
				self.taxon.quasiType = self.callerQT

		self.addTask(TaskCallerType(self.getCaller(), self.getArguments()))
