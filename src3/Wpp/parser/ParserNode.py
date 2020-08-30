from core.operators import opcodeMap

namedOps = {'as'}

class ParserNode:
	def __init__(self, lexType, value):
		self.lexType = lexType # cmd, id, int, fixed, float
		self.txType = '' # const, named, unop, binop
		self.value = value
		self.args = []
		self.prior = 0

	def isOp(self):
		return (self.lexType in {'cmd'}) or (self.lexType == 'id' and self.value in namedOps)

	def isArg(self):
		return (self.lexType in {'int', 'fixed', 'float', 'string'}) or (self.lexType == 'id' and self.value not in namedOps)

	def setArgType(self):
		""" Назначить тип аргумента """
		if self.lexType in {'int', 'float', 'fixed', 'string'}:
			self.txType = 'const'
		elif self.lexType == 'id':
			if self.value in {'true', 'false', 'null'}:
				self.txType = 'const'
			else:
				self.txType = 'named'

	def initOp(self, context):
		descr = opcodeMap.get(self.value)
		if not descr:
			context.throwError('Invalid operation "%s"' % self.value)
		opcode, name, txType, prior = descr
		self.txType = txType
		self.prior = prior

	def __str__(self):
		s = '%s:%s' % (self.txType, self.value)
		if len(self.args) > 0:
			s += '(%s)' % ', '.join([str(n) for n in self.args])
		return s

	def createTaxon(self, context):
		from Wpp.WppExpression import WppConst, WppNamed, WppCall, WppThis, WppMemberAccess, WppBinOp
		if self.txType == 'const':
			return WppConst.create(self.value)
		if self.txType == 'named':
			if self.value == 'this':
				return WppThis()
			return WppNamed(self.value)
		if self.txType == 'call':
			taxon = WppCall()
			for arg in self.args:
				taxon.addItem(arg.createTaxon(context))
			return taxon
		if self.txType == 'binop':
			if self.value == '.':
				taxon = WppMemberAccess(self.args[1].value)
				taxon.addItem(self.args[0].createTaxon(context))
				return taxon
			taxon = WppBinOp(self.value)
			taxon.addItem(self.args[0].createTaxon(context))
			taxon.addItem(self.args[1].createTaxon(context))
			return taxon

		context.throwError('Cant create expression %s' % self)
