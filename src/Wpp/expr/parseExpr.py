from Wpp.expr.operations import specChars, specWords

slash = {
	'\\': '\\',
	'\"': '\"',
	'\'': '\'',
	'n': '\n',
	't': '\t',
	'r': '\r',
}

def parseExpr(text, context):
	""" Разобрать строку выражения на лексемы
	Результат: список лексем.
	Каждая лексема описывается кортежем из 3 элементов: (value, lexemType, constType)
	"""
	text += ' '
	commands, state = [], 'space'
	i, n, value = 0, len(text), ''
	type1, type2 = None, None

	while i < n:
		ch = text[i]
		i += 1
		if state == 'space':
			if ch.isdigit():
				state, value = 'number', ch
			elif ch.isalpha():
				state, value = 'id', ch
			elif ch == '"':
				state, value = 'string', ''
			elif ch in specChars:
				state, value = 'spec', ch
			elif ch not in {' ', '\t'}:
				context.throwError('Invalid character "' + ch + '" in expression ' + text[0:-1])
		elif state == 'number':
			if ch.isdigit():
				value += ch
			elif ch == '.':
				state = 'fixed'
				value += ch
			elif ch=='E' or ch=='e':
				state = 'float'
				value += 'E'
			else:
				type1, type2 = 'const', 'int'
		elif state == 'fixed':
			if ch >= '0' and ch <= '9':
				value += ch
			elif ch=='E' or ch=='e':
				state = 'float'
				value += 'E'
			else:
				type1, type2 = 'const', 'fixed'
		elif state == 'float':
			if ch.isdigit() or (value[-1]=='E' and ch in '+-'):
				value += ch
			else:
				type1, type2 = 'const', 'float'
		elif state == 'spec':
			if (value in specWords) and (value+ch not in specWords):
				type1 = 'cmd'
			elif ch in specChars:
				value += ch
			else:
				context.throwError('Invalid operator '+value)
		elif state == 'id':
			if ch.isalnum():
				value += ch
			else:
				type1 = 'id'
		elif state == 'string':
			if i == n:
				raise context.throwError('String is not closed')
			if ch=='\\':
				state = 'slash'
			elif ch=='"':
				i += 1
				type1, type2 = 'const', 'string'
			else:
				value += ch
		elif state == 'slash':
			if i == n:
				context.throwError('String is not closed')
			if ch in slash:
				value += slash[ch]
				state = 'string'
			else:
				context.throwError('Invalid escape char: '+ch)

		if type1:
			state = 'space'
			i -= 1
			commands.append((value, type1, type2))
			value, type1, type2 = '', None, None

	commands.append(('end', 'cmd', None))
	return commands
