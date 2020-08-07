from core.TaxonExpression import TaxonConst, TaxonNamed, TaxonCall
from Wpp.parser.parseLexems import parseLexems
from core.QuasiType import QuasiType
from core.TaxonOverload import TaxonOverload
from utils.drawTaxonTree import drawTaxonTree

def fromLexems(lexems, pos, context):
	# Заглушка 2
	value, lexType = lexems[pos]
	v1, t1 = lexems[pos]
	v2, t2 = lexems[pos+1] if pos +1 < len(lexems) else (None, None)
	expr = None
	if lexType == 'id':
		if value in ('true', 'false', 'null'):
			expr = WppConst.create(value)
		elif v2 != '(':
			expr = WppNamed(value)
	elif lexType in ('int', 'float', 'fixed', 'string'):
		expr = WppConst.create(value)
	if expr:
		return (expr, pos + 1)

	if t1 == 'id' and v2 == '(':
		expr = WppCall()
		expr.addItem(WppNamed(v1))
		pos += 2
		if lexems[pos][0] == ')':
			return (expr, pos + 1)
		while True:
			param, pos = fromLexems(lexems, pos, context)
			expr.addItem(param)
			v3, t3 = lexems[pos]
			if v3 == ',':
				pos += 1
				continue
			if v3 == ')':
				return (expr, pos + 1)
			break
	context.throwError('Invalid expression: ' + ' '.join([v for v, t in lexems]))

class WppExpression:
	@staticmethod
	def parse(expression, context):
		# Пока что заглушка. Считаем, что все выражения являются константами либо именами
		# if expression not in ('true', 'false', 'null') and expression[0].isalpha():
		# 	return WppNamed(expression)
		# return WppConst.create(expression)
		lexems = parseLexems(expression, context)
		expr, pos = fromLexems(lexems, 0, context)
		return expr


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
		self.addTask(TaskBindTarget())

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
		exprCode = context.currentLine.split(' ', 1)[1].strip()
		expr = WppExpression.parse(exprCode, context)
		# drawTaxonTree(expr)
		# Скопировать подчиненные элементы из созданного выражения к себе
		for item in expr.items:
			self.addItem(item)

	def export(self, outContext):
		outContext.writeln('call ' + self.exportString())

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
				else:
					formalParams = target.getParamsList()
					# Если фактических параметров больше, чем формальных, это ошибка
					if len(self.args) > len(formalParams):
						self.taxon.throwError('%s() takes %d argument but %d were given' % (target.getName(), len(formalParams), len(self.args)))
					for i, param in enumerate(formalParams):
						if i >= len(self.args):
							if not param.getValueTaxon():
								# Если фактических параметров меньше, чем нужно
								self.taxon.throwError('%s() missing required argument: "%s"' % (target.getName(), param.getName()))
						else:
							# Проверять типы аргументов
							result, errorMsg = QuasiType.matchTaxons(param, self.args[i])
							if errorMsg:
								self.taxon.throwError(errorMsg)
				
				self.taxon.quasiType = self.callerQT

		self.addTask(TaskCallerType(self.getCaller(), self.getArguments()))
