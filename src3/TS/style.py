
# a = up, r = down, v = value, f = nextValue (for pair), b = break, n = new line
# a,n = hard up

style = {
	'useTabs': False,
	'tabSize': 4,
	'printWidth': 120,
	'singleQuote': True,
	'cvt': {
		'binop': ' \v ',
		'bodyBegin': ' \v\a\n',
		'bodyEnd': '\r\v',
		'bodyEnd+keyword': '\r\v \f',
		'keyword+bracketBegin': '\v \f',
		'colon': '\v ',
		'instrDiv': '\v\n',
		'itemDiv': '\v \b',
		'ternop': ' \v ',
		'paramDiv': '\v \b',
		'paramsBegin+paramsEnd': '\v\f',
		'paramsBegin': '\v\a',
		'paramsEnd': '\r\v',
	},
	'vertCvt': {
		'paramDivLast': ',\n',
	},
}
