
# static getValue(name: string, defaultValue?: string): string {
#   const value = ParamsManager.getParams()[name];
#   return value === undefined ? defaultValue || '' : value;
# }

example1 = [
	('static', 'keyword'), (' ', 'space'), ('getValue', 'funcName'), ('(', 'paramsBegin'),
	('name', 'paramName'), (':', 'colon'), ('string', 'typeName'), (',', 'paramDiv'),
	('defaultValue', 'paramName'), ('?', 'optional'), (':', 'colon'), ('string', 'typeName'), (',', 'paramDiv'),
	('list', 'varName'), (':','colon'), ('Array', 'typeName'), ('<','arrayBegin'), ('index', 'varName'), ('>','arrayEnd'), ('', 'paramDivLast'),
	(')', 'paramsEnd'), (':', 'colon'), ('string', 'typeName'), ('{', 'bodyBegin'),
	('const', 'keyword'), (' ', 'space'), ('value', 'varName'), ('=', 'binop'), ('ParamsManager', 'typeName'), ('.', 'dot'),
	('getParams', 'funcName'), ('()', 'paramsEmpty'),
	('[', 'arrayBegin'), ('name', 'varName'), (']', 'arrayEnd'), (';', 'instrDiv'),
	('return', 'keyword'), (' ', 'space'), ('value', 'varName'), ('===', 'binop'), ('undefined', 'keyword'),
	('?', 'ternop'), ('defaultValue', 'varName'), ('||', 'binop'), ("''", 'string'), (':', 'ternop'), ('value', 'varName'), (';', 'instrDiv'),
	('}', 'bodyEnd'), ('', 'eof')
]

# Если вывести в одну строку все значения лексем, то получится корректный код. Но без форматирования.

SPC = '·'

rules = {
	'tabSize': 4,
	'printWidth': 180,
}
# a = up, r = down, v = value, f = nextValue (for pair), b = break, n = new line
# a,n = hard up
styles = {
	'instrDiv': '\v\n',
	'bodyBegin': ' \v\a\n',
	'bodyEnd': '\r\v',
	'colon': '\v ',
	'binop': ' \v ',
	'ternop': ' \v ',
	'paramDiv': '\v \b',
	'paramsBegin+paramsEnd': '\v\f',
	'paramsBegin': '\v\a',
	'paramsEnd': '\r\v',
}
levels = {
	'paramsBegin': 'upPost',
	'paramsEnd': 'downPre',
}

def getIndent(level):
	return SPC * (level * rules['tabSize'])

# convert lexems to strings list
def export(lexems):
	rows = ['']
	pos = 0
	curLevel = 0
	while pos < len(lexems) - 1:
		curLevel = applyStyles(lexems[pos], lexems[pos + 1], rows, curLevel)
		pos += 1
	return rows

# -----------------------------------------

def out(outRows, level, value):
	lastIndex = len(outRows) - 1
	if outRows[lastIndex] == '':
		outRows[lastIndex] += getIndent(level)
	outRows[lastIndex] += value

def createLine(outRows):
	outRows.append('')

def setLastRow(outRows, value):
	outRows[len(outRows) - 1] = value

def getLastRow(outRows):
	return outRows[len(outRows)-1]

def getLastRowLength(outRows):
	return len(getLastRow(outRows))

def applyStyle(lexems, pos, isVertival):
	""" Возвращает строку, содержащую escape-символы [n,a,b,r] и приращение позиции"""
	value, cmd = lexems[pos]
	nextValue, nextCmd = lexems[pos+1]
	# Пара имеет приоритет выше, чем одиночное правило
	pairKey = '%s+%s' % (cmd, nextCmd)
	rule = styles.get(pairKey)
	if rule != None:
		return (rule.replace('\v', value).replace('\f', nextValue), 2)
	rule = styles.get(cmd)
	if rule != None:
		return (rule.replace('\v', value), 1)
	return (value, 1)

def processLevel(outRows, lexems, pos, level):
	""" return pos """
	createLine(outRows)
	localLevel = level
	upState = None
	while pos < len(lexems) and lexems[pos][1] != 'eof':
		value, deltaPos = applyStyle(lexems, pos, localLevel == level)
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
					pos, right = processLevel(outRows, lexems, pos, level + 1)
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
				if getLastRowLength(outRows) > rules['printWidth'] and upState != None:
					svPos, svRow = upState
					upState = None
					setLastRow(outRows, svRow)
					pos, value = processLevel(outRows, lexems, svPos, level + 1)
					j=0
					continue
				else:
					out(outRows, level, c)
			j += 1
	return (pos, '')

def draw(rows):
	for s in rows:
		print(s)

stream = []
processLevel(stream, example1, 0, 0)
draw(stream)
