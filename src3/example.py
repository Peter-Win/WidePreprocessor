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
	field public x: double
	field public y: double
	field public static eps: double = 0.001
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const +: Point
		param right: const ref Point
		return Point(x + right.x, y + right.y)
	method static is0: bool
		param value: double
		return value < eps

func init
	var const a: Point = Point(11, 22)
	var const b: Point = a + Point(0, -1)
func main
	init()
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

