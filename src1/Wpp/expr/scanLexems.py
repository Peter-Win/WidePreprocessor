from Wpp.expr.Node import Node
from Wpp.expr.operations import binOps, unOps, ternaryPrior, fnArgsPrior, squareBracketPrior

def scanLexems(lexems, pos, terminators, context):
	"Анализ списка лексем. На выходе единственный узел и позиция последней использованной лекскмы"
	stack = []
	step = 1
	while pos < len(lexems):
		value, lexemType, constType = lexems[pos]
		# Проверка на команду - завершитель
		if lexemType == 'cmd' and value in terminators:
			break
		pos += 1
		if stack and stack[-1].isSpecMinus(lexemType, constType):
			# Специальный случай - замена унарного минуса к числовой константе на отрицательное число 
			stack[-1] = Node('arg', lexemType, '-'+value, constType, True)
		elif lexemType == 'const' or lexemType == 'id':
			stack.append(Node('arg', lexemType, value, constType, True))
		elif lexemType == 'cmd':
			if stack and stack[-1].bArgument:
				if value == '?':
					prior = ternaryPrior
					optimizeStack(stack, prior, context)
					opNode = Node('ternar', lexemType, prior=prior)
					opNode.args.append(stack.pop())
					arg2, pos = scanLexems(lexems, pos, {':'}, context)
					pos += 1
					opNode.args.append(arg2)
				elif value == '(':
					# Вызов функции
					prior = fnArgsPrior
					optimizeStack(stack, prior, context)
					opNode = Node('call', lexemType, prior=prior, bArgument=True)
					opNode.args.append(stack.pop())
					if lexems[pos][0] == ')':
						pos += 1
					else:
						while True:
							aNode, pos = scanLexems(lexems, pos, {',', ')'}, context)
							termCmd, termType, termX = lexems[pos]
							opNode.args.append(aNode)
							pos += 1
							if termCmd == ')':
								break
				elif value == '[':
					prior = squareBracketPrior
					optimizeStack(stack, prior, context)
					opNode = Node('index', lexemType, prior=prior)
					opNode.args.append(stack.pop())
					aNode, pos = scanLexems(lexems, pos, {']'}, context)
					opNode.args.append(aNode)
					pos += 1
				else:
					# Бинарный оператор
					prior = binOps.get(value)
					if not prior:
						context.throwError('Invalid binary operation ' + value)
					optimizeStack(stack, prior, context)
					opNode = Node('binop', lexemType, value, prior=prior)
					opNode.args.append(stack.pop())
				stack.append(opNode)
			else:
				# Унарный оператор
				if value == '(':
					# Скобки для группировки операций
					opNode, pos = scanLexems(lexems, pos, {')'}, context)
					pos += 1
				elif value == '[':
					# Значение типа массива
					opNode, pos = createArray(lexems, pos, context)
				else:
					prior = unOps.get(value)
					if not prior:
						context.throwError('Invalid unary operation ' + value)
					optimizeStack(stack, prior, context)
					opNode = Node('unop', lexemType, value, prior=prior)
				stack.append(opNode)
	if pos == len(lexems):
		context.throwError('No end of expression found')
	optimizeStack(stack, 100, context)
	if len(stack) != 1:
		# Если узлы не сошлись в один, то это неправильное выражение. Типа x 1
		context.throwError('Invalid expression: [' + ', '.join([str(i) for i in stack])+']')
	return (stack[0], pos)

def createArray(lexems, pos, context):
	value = Node('array', 'array', bArgument = True)
	divider = ''
	while divider != ']':
		node, pos = scanLexems(lexems, pos, {',', ']'}, context)
		divider, t, x = lexems[pos]
		value.args.append(node)
		pos += 1
	return value, pos

def optimizeStack(stack, prior, context):
	if not stack:
		return

	while True:
		last = stack.pop()
		if not last.bArgument:
			stack.append(last)
			return
		if not stack:
			stack.append(last)
			return
		op = stack.pop()
		if op.bArgument:
			context.throwError('Expected operation instead of '+str(op))
		if op.prior > prior:
			stack.append(op)
			stack.append(last)
			return
		op.args.append(last)
		op.bArgument = True
		stack.append(op)
