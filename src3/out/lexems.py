class Lex:
	arrayBegin = ('[', 'arrayBegin')
	arrayEnd = (']', 'arrayEnd')
	bodyBegin = ('{', 'bodyBegin')
	bodyEnd = ('}', 'bodyEnd')
	bracketBegin = ('(', 'bracketBegin')
	bracketEnd = (')', 'bracketEnd')
	colon = (':', 'colon')
	dot = ('.', 'dot')
	instrDiv = (';', 'instrDiv')
	itemDiv = (',', 'itemDiv')
	itemDivLast = ('', 'itemDivLast')
	objBegin = ('{', 'objBegin')
	objEnd = ('}', 'objEnd')
	paramDiv = (',', 'paramDiv')
	paramDivLast = ('', 'paramDivLast')
	paramsBegin = ('(', 'paramsBegin')
	paramsEnd = (')', 'paramsEnd')
	space = (' ', 'space')
	eol = ('\n', 'eol')

	@staticmethod
	def indent(level, rules):
		offset = level * '\t' if rules['useTabs'] else (level * rules['tabSize']) * ' '
		return (offset, 'space')

	@staticmethod
	def binop(name):
		return (name, 'binop')

	@staticmethod
	def fieldName(name):
		return (name, 'fieldName')

	@staticmethod
	def funcName(name):
		return (name, 'funcName')

	@staticmethod
	def keyword(name):
		return (name, 'keyword')

	@staticmethod
	def typeName(name):
		return (name, 'typeName')

	@staticmethod
	def varName(name):
		return (name, 'varName')

	@staticmethod
	def className(name):
		return (name, 'className')

	@staticmethod
	def slashes(text):
		return ('//'+text, 'comment')

	@staticmethod
	def stringRaw(value, rules):
		return (Lex.quoted(value, rules), 'string')

	@staticmethod
	def quoted(value, rules):
		q = "'" if rules['singleQuote'] else '"'
		return '%s%s%s' % (q, value, q)
