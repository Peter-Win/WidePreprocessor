class Lex:
	arrayBegin = ('[', 'arrayBegin')
	arrayEnd = (']', 'arrayEnd')
	bodyBegin = ('{', 'bodyBegin')
	bodyEnd = ('}', 'bodyEnd')
	colon = (':', 'colon')
	instrDiv = (';', 'instrDiv')
	itemDiv = (',', 'itemDiv')
	objBegin = ('{', 'objBegin')
	objEnd = ('}', 'objEnd')
	paramDiv = (',', 'paramDiv')
	paramDivLast = ('', 'paramDivLast')
	paramsBegin = ('(', 'paramsBegin')
	paramsEnd = (')', 'paramsEnd')
	space = (' ', 'space')
	eol = ('\n', 'eol')

	@staticmethod
	def binop(name):
		return (name, 'binop')

	@staticmethod
	def fieldName(name):
		return (name, 'fieldName')

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
	def slashes(text):
		return ('//'+text, 'comment')
