multiCmd = {'==', '!=', '<=', '>=', '&&', '||', '**', '<<', '>>'}

def parseLexems(row, context):
	j = 0
	lexems = []
	state = 'space'
	value = ''
	while j < len(row):
		ch = row[j]
		if state == 'space':
			if ch.isalpha():
				state = 'id'
			elif ch.isdigit():
				state = 'int'
			elif ch in '-+*/<>()[].,;!&|=':
				state = 'cmd'
			elif ch not in ' \t':
				context.throwError('Invalid character "%s"' % ch)
			value = ch

		elif state == 'id':
			if not ch.isalpha() and not ch.isdigit() and ch != '_':
				lexems.append((value, state))
				state = 'space'
				continue
			value += ch
		elif state == 'int':
			if ch == '.':
				state = 'fixed'
			elif not ch.isdigit():
				lexems.append((value, state))
				state = 'space'
				continue
			value += ch
		elif state == 'fixed':
			if ch in 'eE':
				state = 'float'				
			elif not ch.isdigit():
				lexems.append((value, state))
				state = 'space'
				continue
			value += ch
		elif state == 'float':
			if ((value[-1] in 'eE') and (ch in '-+')) or ch.isdigit():
				value += ch
			else:
				lexems.append((value, state))
				state = 'space'
				continue
		elif state == 'cmd':
			if value == '-' and ch.isdigit():
				state = 'int'
				continue
			multiCase = value + ch
			if multiCase in multiCmd:
				value = multiCase
				j += 1
				continue
			lexems.append((value, state))
			state = 'space'
			continue
		j += 1
	if state != 'space':
		lexems.append((value, state))
	return lexems
