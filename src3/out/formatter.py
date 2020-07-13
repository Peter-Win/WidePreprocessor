# Формат объекта стиля
# useTabs: boolean
# tabSize: int
# printWidth: int
# cvt, vertCvt: Map<string, string> транслируют коды (второй элемент лексемы) в строку формата, содержащую escape-символы
# Escape-символы 
# a = up, r = down, v = value, f = nextValue (for pair), b = break, n = new line
# a,n = hard up

def getIndent(level, style):
	if style['useTabs']:
		return level * '\t'
	return ' ' * (level * style['tabSize'])

def out(outRows, level, value, style):
	lastIndex = len(outRows) - 1
	if outRows[lastIndex] == '':
		outRows[lastIndex] += getIndent(level, style)
	outRows[lastIndex] += value

def createLine(outRows):
	outRows.append('')

def setLastRow(outRows, value):
	outRows[len(outRows) - 1] = value

def getLastRow(outRows):
	return outRows[len(outRows)-1]

def getLastRowLength(outRows, style):
	length = 0
	j = 0
	s = getLastRow(outRows)
	while j < len(s):
		if s[j] == '\t':
			length += style['tabSize']
		else:
			length += 1
		j += 1
	return length

def applyStyle(lexems, pos, isVertical, style):
	""" Возвращает строку, содержащую escape-символы [n,a,b,r] и приращение позиции"""
	value, cmd = lexems[pos]
	if pos < len(lexems)-1:
		nextValue, nextCmd = lexems[pos+1]
		# Пара имеет приоритет выше, чем одиночное правило
		pairKey = '%s+%s' % (cmd, nextCmd)
		rule = style['cvt'].get(pairKey)
		if rule != None:
			return (rule.replace('\v', value).replace('\f', nextValue), 2)
	rule = style['cvt'].get(cmd)
	if rule != None:
		return (rule.replace('\v', value), 1)
	return (value, 1)

def formatLexems(outRows, lexems, pos, level, style):
	""" return pos """
	createLine(outRows)
	localLevel = level
	upState = None
	while pos < len(lexems) and lexems[pos][1] != 'eof':
		value, deltaPos = applyStyle(lexems, pos, localLevel == level, style)
		prevPos = pos
		pos += deltaPos
		j = 0
		while j < len(value):
			c = value[j]
			if c == '\a':
				if j < len(value) - 1 and value[j+1] == '\n':
					# Принудительное повышение уровня
					# TODO: Вероятно, иммет смысл лишь при условии localLevel == level
					# TODO: пока остаток строки пропадает
					pos, right = formatLexems(outRows, lexems, pos, level + 1, style)
					j = 0
					value = right
					continue
				elif localLevel == level:
					# Если происходит повышение с главного уровня, то надо запомнить текущее состояние
					upState = (pos, getLastRow(outRows))
				localLevel += 1
			elif c == '\r':
				localLevel -= 1
				# Если уровень спускается ниже основного, то конец функции
				if localLevel < level:
					createLine(outRows)
					return (pos, value[j+1:])
			elif c == '\b':
				if localLevel == level:
					createLine(outRows)
			elif c == '\n':
				createLine(outRows)
			else:
				# Проверка на выход за границы printWidth
				if getLastRowLength(outRows, style) > style['printWidth'] and upState != None:
					svPos, svRow = upState
					upState = None
					setLastRow(outRows, svRow)
					pos, value = formatLexems(outRows, lexems, svPos, level + 1, style)
					j=0
					continue
				else:
					out(outRows, level, c, style)
			j += 1
	return (pos, '')
