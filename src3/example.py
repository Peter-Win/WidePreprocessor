from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from utils.drawTaxonTree import drawTaxonTree
import json

def printCtx(ctx):
	for line in ctx.lines:
		print(line)

def exportTS(module):
	from TS.TSCore import TSCore
	from TS.style import style
	print('-- TypeScript')
	tsModule = TSCore.createFromSource(module)
	outCtx = OutContextMemoryStream()
	tsModule.exportContext(outCtx, style)
	printCtx(outCtx)
	# Debug output lexems to JSON

	lexems = []
	tsModule.exportLexems(lexems, style)
	rows = ['[']
	for lex in lexems:
		rows.append('  ["%s", "%s"],' % lex)
	rows[-1] = rows[-1][0:-1]
	rows.append(']')
	f = open('lexems.json', 'w')
	for s in rows:
		f.write("%s\n" % s);
	f.close()
	with open("style.json", "w") as write_file:
		json.dump(style, write_file, ensure_ascii=False, indent=4)


def exportPy(module):
	from Python.PyCore import PyCore
	from Python.style import style
	print('-- Python')
	pyModule = PyCore.createFromSource(module)
	outCtx = OutContextMemoryStream()
	pyModule.exportContext(outCtx, style)
	printCtx(outCtx)

source = """
class simple Point
	field x: double
	field y: double
	constructor
		autoinit x
		autoinit y
	operator const overload +: Point
		altName addPt
		param p: Point
		return Point(x + p.x, y + p.y)
	operator const overload +: Point
		altName addN
		param k: double
		return Point(x + k, y + k)
	method const overload plus: Point
		altName plusPt
		param p: const ref Point
		return Point(x + p.x, y + p.y)
	method const overload plus: Point
		altName plusN
		param k: double
		return Point(x + k, y + k)
var const a: Point = Point(11, 22) + 3
var const b: Point = a + Point(-1, -2)
var const a1: Point = Point(11, 22).plus(3)
var const b1: Point = a1.plus(Point(-1, -2))
"""

print('-- Wpp')
module = WppCore.createMemModule(source, 'example.wpp')
outCtx = OutContextMemoryStream()
module.export(outCtx);
print(str(outCtx))

print('')
exportTS(module)

print('')
exportPy(module)

