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
class public simple Point
	# 2D coordinates
	field public x: double
		# field comment
	field public y: double
	field static flag: bool
	method const isValid: bool
		# method comment
		if x
			return true
		elif y
			return true
		return false

	method static test: bool
		param bUpdate: bool = false
		return flag
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
