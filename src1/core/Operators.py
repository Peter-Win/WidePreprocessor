UnOpNames = {
	'-': 'neg',
	'~': 'invert',
}

BinOpNames = {
	'<': 'lt',
	'<=': 'le',
	'>': 'gt',
	'>=': 'ge',
	'==': 'eq',
	'!=': 'ne',
	'+': 'add',
	'-': 'sub',
	'*': 'mul',
	'/': 'div',
	'%': 'mod',
	'**': 'pow',
	'<<': 'lshift',
	'>>': 'rshift',
	'&': 'and',
	'^': 'xor',
	'|': 'or',
	'+=': 'iadd',
	'-=': 'isub',
	'*=': 'imul',
	'/=': 'idiv',
	'%=': 'imod',
	'**=': 'ipow',
	'<<=': 'ilshift',
	'>>=': 'irshift',
	'&=': 'iand',
	'^=': 'ixor',
	'|=': 'ior',
}

def forSameType(ops, types):
	result = []
	for opId in ops:
		for t in types:
			result.append((opId, t, t, t))
	return result

StdBinOps = forSameType(['+', '-', '*', '/'], ['int', 'float', 'double'])