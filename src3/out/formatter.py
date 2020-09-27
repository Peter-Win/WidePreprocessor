"""
\\v - value
\\n - new line
\\bU - level up
\\bD - level down
"""
def insertValues(rule, value1, value2 = ''):
	result = ''
	n = 0
	for c in rule:
		if c == '\v':
			if n == 0:
				result += value1
			elif n == 1:
				result += value2
			n += 1
		else:
			result += c
	return result

def applyStyle(lexems, pos, style):
	value, cmd = lexems[pos]
	if pos < len(lexems) - 1:
		nextValue, nextCmd = lexems[pos + 1]
		# Пара имеет приоритет выше, чем одиночное правило
		pairKey = cmd + '+' + nextCmd
		rule = style['cvt'].get(pairKey)
		if rule:
			return insertValues(rule, value, nextValue), 2
	rule = style['cvt'].get(cmd)
	if rule:
		return insertValues(rule, value), 1
	return value, 1

def formatLexems(outRows, lexems, pos, level, style):
	def createLine():
		outRows.append('')
	def outChar(c):
		if len(outRows[-1]) == 0:
			indent = '\t' * level if style['useTabs'] else ' ' * (level * style['tabSize'])
			outRows[-1] += indent
		outRows[-1] += c
	createLine()
	while pos < len(lexems):
		value, deltaPos = applyStyle(lexems, pos, style)
		pos += deltaPos
		isCmd = False
		for c in value:
			if isCmd:
				if c == 'U':
					level += 1
				elif c == 'D':
					level -= 1
				isCmd = False
			elif c == '\n':
				createLine()
			elif c == '\b':
				isCmd = True
			else:
				outChar(c)
