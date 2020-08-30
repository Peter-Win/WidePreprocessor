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
var const a: double = 1
var const b: double = 2
# var const c: double = a + b * 3
# var const d: double = (a + b) * c
# var const e: double = a + (b * c)
"""
source1 = """
class simple Point
	field x: double
	field y: double
	constructor
		autoinit x
		autoinit y
"""
source1 = """
class simple Point
	field x: double
	field y: double
	constructor overload
		autoinit x
		autoinit y
	constructor overload
		param pt: const ref Point
		x = pt.x
		y = pt.y
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

