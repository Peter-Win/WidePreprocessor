import unittest
from TS.style import style
from out.formatter import formatLexems
from out.lexems import Lex

class TestTSStyle(unittest.TestCase):
	@unittest.skip('Fix later')
	def testParams(self):
		style['printWidth'] = 1000
		# function applyStyle(lexems: Lexem[], pos: number, isVertical: boolean, style: Styles): {value: string, pos: number} {}
		lexems = [('function', 'keyword'), Lex.space, ('applyStyle', 'funcName'), Lex.paramsBegin,
			('lexems', 'varName'), Lex.colon, ('Lexem', 'typeName'), Lex.arrayBegin, Lex.arrayEnd, Lex.paramDiv,
			('pos', 'varName'), Lex.colon, Lex.typeName('number'), Lex.paramDiv,
			Lex.varName('isVertical'), Lex.colon, Lex.typeName('boolean'), Lex.paramDiv,
			Lex.varName('style'), Lex.colon, Lex.typeName('Styles'), Lex.paramsEnd,
			Lex.colon, Lex.objBegin, Lex.fieldName('value'), Lex.colon, Lex.typeName('string'), Lex.itemDiv,
			Lex.fieldName('pos'), Lex.colon, Lex.typeName('number'), Lex.objEnd,
			Lex.bodyBegin, Lex.bodyEnd,
		]
		outRows = []
		formatLexems(outRows, lexems, 0, 0, style)
		# for row in outRows:
		# 	print('<<<%s>>>' % row.replace(' ', '_'))
		self.assertEqual(outRows, [
			"function applyStyle(lexems: Lexem[], pos: number, isVertical: boolean, style: Styles): {value: string, pos: number} {", "}"
		])