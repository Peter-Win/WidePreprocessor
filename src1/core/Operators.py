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

def addOperator(taxonOperator, taxonOwner):
	name = taxonOperator.name
	over = taxonOwner.dictionary.get(name)
	if not over:
		if hasattr(taxonOwner, 'taxonMap'):
			over = taxonOwner.taxonMap['Overloads'](name)
		else:
			over = taxonOwner.creator('Overloads')(name)
		taxonOwner.addNamedItem(over)
	over.addItem(taxonOperator)

def createOperator(descr, core):
	opId, leftType, rightType, resultType = descr
	taxonOp = core.taxonMap['Operator'](name = opId)
	# Empty body
	taxonOp.addItem(core.taxonMap['Block']())
	# result type
	result = core.taxonMap['TypeName'](resultType)
	taxonOp.addItem(result)
	#left param
	left = core.taxonMap['Param']('left')
	left.addItem(core.taxonMap['TypeName'](leftType))
	taxonOp.addNamedItem(left)
	# right param
	right = core.taxonMap['Param']('right')
	right.addItem(core.taxonMap['TypeName'](rightType))
	taxonOp.addNamedItem(right)
	return taxonOp

def createOperatorLow(core, opId, leftType, rightType, resultType):
	taxonOp = core.taxonMap['Operator'](name = opId)
	# Empty body
	taxonOp.addItem(core.taxonMap['Block']())
	# result 
	taxonOp.addItem(resultType)
	#left param
	left = core.taxonMap['Param']('left')
	left.addItem(leftType)
	taxonOp.addNamedItem(left)
	# right param
	right = core.taxonMap['Param']('right')
	right.addItem(rightType)
	taxonOp.addNamedItem(right)
	return taxonOp


def forSameType(ops, types):
	result = []
	for opId in ops:
		for t in types:
			result.append((opId, t, t, t))
	return result

def _boolOps(ops, types):
	result = []
	for opId in ops:
		for t in types:
			result.append((opId, t, t, 'bool'))
	return result

# Array<(opId, leftType, rightType, resultType)>
StdBinOps = \
	forSameType(['+', '-', '*', '/'], ['int', 'long', 'float', 'double']) + \
	_boolOps(['==', '!=', '<', '>', '<=', '>='], ['int', 'long', 'float', 'double']) + \
	[
		('+', 'String', 'String', 'String'),
		('+', 'String', 'long', 'String'),
	]
