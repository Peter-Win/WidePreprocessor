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
var const public myInt: int = 22
var const public myLong: long = -123456
var public myFloat: float = 1.23
var public myDouble: double = -1.23E+04
var myTrue: bool = true
var myFalse: bool = false
var defInt: int
var defULong: unsigned long
var defFloat: float
var defDouble: double
var defBool: bool

func public firstFunc: int
	param x: int
	param y: int = 100
	# This is first function.
	# Second line.
	if x
		return x
	return y

func public secondFunc: int
	param x: int
	return firstFunc(x)

func public thirdFunc
	param x: int
	call firstFunc(x)
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
