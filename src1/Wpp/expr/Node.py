class Node:
	""" Внутренний класс.
	Используется только для анализа лексем выражения
	"""
	def __init__(self, type, lexemType, value=None, constType=None, bArgument=False, prior=100):
		self.type = type
		self.lexemType = lexemType
		self.constType = constType
		self.bArgument = bArgument
		self.value = value
		self.prior = prior
		self.args = []

	def update(self):
		if self.type == 'binop' and self.value == '.':
			second = self.args[1]
			if second.lexemType == 'id':
				second.lexemType = 'field'
		for a in self.args:
			a.update()

	def isSpecMinus(self, lexemType, constType):
		return self.type == 'unop' and self.value == '-' and lexemType == 'const' and constType in {'int', 'fixed', 'float'}

	def makeTaxon(self):
		from Wpp.expr.Taxons import WppArrayIndex, WppArrayValue, WppBinOp, WppCall, WppConst, WppFalse, WppFieldExpr, WppIdExpr, WppNull, WppTernaryOp, WppThis, WppTrue, WppSuper, WppUnOp
		keyWords = {'this': WppThis, 'super': WppSuper, 'true': WppTrue, 'false': WppFalse, 'null': WppNull}

		if self.type == 'array':
			taxon = WppArrayValue()
			for arg in self.args:
				taxon.addItem(arg.makeTaxon())
			return taxon
		if self.lexemType == 'const':
			return WppConst(self.constType, self.value)
		if self.lexemType == 'id':
			Constr = keyWords.get(self.value)
			if Constr:
				return Constr()
			taxon = WppIdExpr()
			taxon.id = self.value
			return taxon
		if self.lexemType == 'field':
			taxon = WppFieldExpr()
			taxon.id = self.value
			return taxon
		if self.type == 'unop':
			taxon = WppUnOp()
			taxon.opCode = self.value
			taxon.prior = self.prior
			taxon.addItem(self.args[0].makeTaxon())
			return taxon
		if self.type == 'binop':
			taxon = WppBinOp()
			taxon.opCode = self.value
			taxon.prior = self.prior
			taxon.addItem(self.args[0].makeTaxon())
			taxon.addItem(self.args[1].makeTaxon())
			return taxon
		if self.type == 'ternar':
			taxon = WppTernaryOp()
			taxon.prior = self.prior
			[taxon.addItem(arg.makeTaxon()) for arg in self.args]
			return taxon
		if self.type == 'call':
			taxon = WppCall()
			taxon.prior = self.prior
			for arg in self.args:
				taxon.addItem(arg.makeTaxon())
			return taxon
		if self.type == 'index': # Array index
			taxon = WppArrayIndex()
			taxon.addItems([arg.makeTaxon() for arg in self.args])
			return taxon
		raise RuntimeError('Invalid operation type: ' + str(self))

	def __str__(self):
		s = self.type + ':' + self.lexemType
		if self.prior:
			s += ':' + str(self.prior)
		if self.value:
			s += '= '
			if self.constType:
				s += self.constType+'('
			s += self.value
			if self.constType:
				s += ')'
		if len(self.args) > 0:
			s += '[' + ', '.join([str(a) for a in self.args]) + ']'
		return s

	def export(self):
		def checkBrackets(node, prior):
			s = node.export()
			if node.type == 'arg' or prior >= node.prior:
				return s
			return '(' + s + ')'
		if self.type == 'arg':
			if self.lexemType == 'const' and self.constType == 'string':
				return '"' + self.value + '"'
			return self.value
		if self.type == 'unop':
			return self.value + checkBrackets(self.args[0], self.prior)
		if self.type == 'binop':
			op = self.value
			if op != '.':
				op = ' '+op+' '
			return checkBrackets(self.args[0], self.prior) + op + checkBrackets(self.args[1], self.prior)
		if self.type == 'ternar':
			a = [checkBrackets(arg, self.prior) for arg in self.args]
			return a[0] + ' ? ' + a[1] + ' : ' + a[2]
		if self.type == 'call':
			s = self.args[0].export() + '('
			s += ', '.join([a.export() for a in self.args[1:]])
			return s + ')'
		if self.type == 'index':
			return checkBrackets(self.args[0], self.prior) + '[' + self.args[1].export() + ']'
		if self.type == 'array':
			return '[' + ', '.join([i.export() for i in self.args]) + ']'

