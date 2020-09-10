from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from utils.drawTaxonTree import drawTaxonTree

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
	field public x: double = 0
var const pt: Point = Point()
var const x: double = pt.x
"""


source1 = """
class simple Point
	field public x: double
	field public y: double
	constructor overload
		x = 0
		y = 0
	constructor overload
		altName initPoint
		autoinit x
		autoinit y
	constructor overload
		altName copyPoint
		param src: const ref Point
		x = src.x
		y = src.y
var const first: Point = Point(1, 2)
var const second: Point = Point(first)
"""

print('-- Wpp')
module = WppCore.createMemModule(source, 'example.wpp')
outCtx = OutContextMemoryStream()
module.export(outCtx);
print(str(outCtx))

print('')
exportPy(module)

print('')
exportTS(module)

