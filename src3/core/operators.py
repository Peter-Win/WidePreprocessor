# Operator names from Python

# opcode, name, type, defaultPrior
# default prior from JavaScript https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence
opsList = [
	('.', 'attr', 'binop', 20),  # in python getattr/setattr
	('[]', 'item', 'binop', 20), # in python getitem/setitem
	('new', 'new', 'new', 20),
	('call', 'call', 'call', 20),
	('!', 'not', 'unop', 17),
	('~', 'invert', 'unop', 17),
	('neg', 'neg', 'unop', 17),
	('**', 'pow','binop', 16),
	('*',  'mul','binop', 15),
	('/',  'div','binop', 15),
	('%',  'mod','binop', 15),
	('+',  'add','binop', 14),
	('-',  'sub','binop', 14),
	('<<', 'lshift', 'binop', 13),
	('>>', 'rshift', 'binop', 13),
	('<',  'lt', 'binop', 12),
	('<=', 'le', 'binop', 12),
	('>',  'gt', 'binop', 12),
	('>=', 'ge', 'binop', 12),
	# instanceof 12
	('==', 'eq', 'binop', 11),
	('!=', 'ne', 'binop', 11),
	('&',  'and', 'binop', 10),
	('^',  'xor', 'binop', 9),
	('|',  'or', 'binop', 8),
	('&&', 'logAnd', 'binop', 7), # Не может переопределяться, т.к. имеет ленивую логику
	('||', 'logOr', 'binop', 6), # Не может переопределяться, т.к. имеет ленивую логику
	('?', 'if', 'ternop', 4), # Не переопределяется в питоне

	('=', 'let', 'binop', 3), # Не переопределяется
	('+=', 'iadd', 'binop', 3),
	('-=', 'isub', 'binop', 3),
	('*=', 'imul', 'binop', 3),
	('/=', 'idiv', 'binop', 3),
	('%=', 'imod', 'binop', 3),
	('**=', 'ipow', 'binop', 3),
	('<<=', 'ilshift', 'binop', 3),
	('>>=', 'irshift', 'binop', 3),
	('&=', 'iand', 'binop', 3),
	('^=', 'ixor', 'binop', 3),
	('|=', 'ior', 'binop', 3),
]

opcodeMap = {item[0]:item for item in opsList}
nameMap = {item[1]:item for item in opsList}

def isAssignOp(opcode):
	return opcode[-1] == '=' and opcode not in ('!=', '<=', '>=', '==')

def findBinOpExt(binOp):
	"""
	Расширенный поиск оператора.
	Сначала проверка левой половины, является ли экземпляром простого класса. В этом случае ищем переопределенный оператор в классе. (без признака right)
	Затем проверка правой половины. Если экземпляр простого класса, то поиск оператора с признаком right.
	И если не надено, тогда поиск в ядре.
	Перед вызовом функции нужно дождаться квази-типов для обоих частей.
	Возвращаемое значение: TaxonOperator | TaxonDeclBinOp | None
	"""
	from core.QuasiType import QuasiType
	opcode = binOp.opcode
	leftQType = binOp.getLeft().buildQuasiType()
	rightQType = binOp.getRight().buildQuasiType()

	def checkCustom(qtPrimary, qtSecondary, isRight):
		if not qtPrimary.taxon.isClass() or 'simple' not in qtPrimary.taxon.attrs:
			return None, None
		decl = qtPrimary.taxon.findMember(opcode)
		if not decl:
			return None, None
		if decl.type == 'operator' and ('right' in decl.attrs) == isRight:
			paramsList = decl.getParamsList()
			if len(paramsList) == 1:
				res, err = QuasiType.matchTaxons(paramsList[0], qtSecondary)
				if res:
					return decl, None
		if decl.type == 'overload':
			matches = []
			for operDecl in decl.items:
				paramsList = operDecl.getParamsList()
				if len(paramsList)==1 and ('right' in operDecl.attrs) == isRight:
					res, err = QuasiType.matchTaxons(paramsList[0].getTypeTaxon(), qtSecondary)
					if res:
						matches.append((res, operDecl))
			if len(matches) == 1:
				return matches[0][1], None
			elif len(matches) > 0:
				exacts = [operDecl for res, operDecl in matches if res=='exact']
				if len(exacts) == 0:
					exacts = [operDecl for res, operDecl in matches if res=='constExact']
				if len(exacts) == 1:
					return exacts[0], None
				return None, 'Multiple declarations for operator %s(%s, %s)' % (opcode, leftQType.getDebugStr(), rightQType.getDebugStr())
		return None, None
	decl, err = checkCustom(leftQType, rightQType, False)
	if decl or err:
		return decl, err
	decl, err = checkCustom(rightQType, leftQType, True)
	if decl or err:
		return decl, err
	return binOp.core.findBinOp(opcode, leftQType, rightQType)
