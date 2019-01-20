from core.TaxonFunc import TaxonOperator
from Python.PyFunc import PyCommonFunc

BinOps = {
	'+': 'add',
	'-': 'sub',
	'*': 'mul',
	'%': 'mod',
	'<<': 'lshift',
	'>>': 'rshift',
	'&': 'and',
	'|': 'xor',
	'^': 'or',

	'+=': 'iadd',
	'-=': 'isub',
	'*=': 'imul',
	'%=': 'imod',

	'<': 'lt',
	'<=': 'le',
	'>': 'gt',
	'>=': 'ge',
	'==': 'eq',
	'!=': 'ne',
}
UnOps = {
	'-': 'neg',
	'!': 'not',
}

class PyOperator(TaxonOperator, PyCommonFunc):
	def onUpdate(self):
		if self.isMethod():
			# Если оператор является методом, то он может быть переопределен
			name = (BinOps if self.isBinary() else UnOps).get(self.name)
			if not name:
				self.throeError('Invalid operator name: '+self.name)
			self.altName = name
		else:
			self.throwError('Not implemented operator')

	def export(self, outContext):
		s = 'def __' + self.altName + '__(self'
		for param in self.getParams():
			s += ', ' + param.getName(self)
		s += '):'
		outContext.writeln(s)
		self.getBody().export(outContext)

