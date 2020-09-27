
# \n - new line, \v - value
# \bU - level up, \bD - level down

style = {
	'useTabs': False,
	'tabSize': 4,
	'printWidth': 120,
	'singleQuote': True,
	'cvt': {
		# 'binop': ' \v ',
		# 'bodyBegin': ' \v\a\n',
		# 'bodyEnd': '\r\v',
		# 'bodyEnd+keyword': '\r\v\n\f',
		# 'keyword+bracketBegin': '\v \f',
		# 'colon': '\v ',
		# 'instrDiv': '\v\n',
		'itemDiv': '\v ',
		# 'ternop': ' \v ',
		# 'paramDiv': '\v \b',
		# 'paramsBegin+paramsEnd': '\v\f',
		# 'paramsBegin': '\v\a',
		# 'paramsEnd': '\r\v',
        "colon": "\v ",
        "paramsEnd": "\v",
        "binop": " \v ",
        "binop+bodyBegin": " \v \v\n\bU", # .=>.{
        "bodyBegin": " \v\n\bU",
        "bodyEnd": "\n\bD\v\n",
        "bodyEnd+instrDiv": "\n\bD\v\v\n",
        "paramDiv": "\v ",
        "instrDiv": "\v\n",
	},
	'vertCvt': {
		'paramDivLast': ',\n',
	},
}
