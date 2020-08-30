from Wpp.parser.ParserNode import ParserNode

def trace(msg, ops, args):
	print(msg, 'ops=[%s]  args=[%s]' % (', '.join(str(i) for i in ops), ', '.join(str(i) for i in args)))

def updateOp(curOp, args, context):
	if curOp.txType == 'binop':
		arg2 = args.pop()
		arg1 = args.pop()
		curOp.args.append(arg1)
		curOp.args.append(arg2)
		args.append(curOp)
	else:
		context.throwError('Invalid operation: %s' % curOp)


def unwind(ops, args, context):
	while len(ops) > 0:
		curOp = ops.pop()
		updateOp(curOp, args, context)
	if len(args) != 1:
		context.throwError('Invalid expression ops(%d), args(%d)' % (len(ops), len(args)))
	return args.pop()

def checkPrior(node, ops, args, context):
	while len(ops) > 0:
		curOp = ops.pop()
		if curOp.prior < node.prior:
			ops.append(curOp)
			ops.append(node)
			return
		updateOp(curOp, args, context)
	ops.append(node)

def buildNodes(lexems, pos, stoppers, context):
	"""
	Сформировать из списка лексем дерево узлов, из которого можно будет потом сформировать таксоны
	lexems - Список лексем (value, lexType). lexType in cmd, id, int, fixed, float
	stoppers - множество возможных признаков конца выражения. Н.р. для параметров функции {',', ')'}
	Возвращает пару: узел и новая позиция
	"""
	ops = []
	args = []
	state = 'start'
	while True:
		if pos >= len(lexems):
			context.throwError('Unexpected end of expression: %s' % ' '.join(a for a, b in lexems))
		value, lexType = lexems[pos]
		pos += 1
		if lexType == 'cmd' and value in stoppers:
			break
		node = ParserNode(lexType, value)
		if state == 'start':
			# Можно ожидать: unop, const, name, (, [
			if node.isArg():
				# Если аргумент, добавить в стек аргументов
				node.setArgType()
				args.append(node)
				state = 'postArg'
			elif value == '(':
				# Скобки для группировки операций (а не список параметров функции)
				node, pos = buildNodes(lexems, pos, {')'}, context)
				args.append(node)
				state = 'postArg'
			else:
				context.throwError('Invalid lexem in expression: "%s"' % (value))
		elif state == 'postArg':
			if value == '(':
				# Это начало параметров функции
				callNode = ParserNode('call', 'call')
				callNode.initOp(context)
				checkPrior(callNode, ops, args, context)
				callNode = ops.pop()
				callNode.args.append(args.pop())
				args.append(callNode)
				if lexems[pos][0] == ')':
					# Пустой список аргументов
					pos += 1
				else:
					while True:
						node, pos = buildNodes(lexems, pos, {',', ')'}, context)
						callNode.args.append(node)
						if lexems[pos-1][0] == ')':
							break
				state = 'postArg'
			elif node.isOp():
				# Это бинарный оператор или точка
				node.initOp(context)
				checkPrior(node, ops, args, context)
				state = 'start'
			else:
				context.throwError('Invalid postArg')

	return unwind(ops, args, context), pos

	