from core.TaxonExpression import TaxonConst, TaxonNamed

class WppExpression:
	@staticmethod
	def parse(expression, context):
		# Пока что заглушка. Считаем, что все выражения являются константами либо именами
		if expression not in ('true', 'false', 'null') and expression[0].isalpha():
			return WppNamed(expression)
		return WppConst.create(expression)

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
				target = self.taxon.findUp(self.taxon.targetName)
				if not target:
					self.taxon.throwError('Not found "%s"' %s (self.taxon.targetName))
				self.taxon.setTarget(target)
		self.addTask(TaskBindTarget())
