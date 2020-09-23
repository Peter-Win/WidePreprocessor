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
var const s: int = 128
var const u: unsigned int = 128
var const sl: int = s << 2
var const ul: unsigned int = u << 2
var const sr: int = s >> 2
var const ur: unsigned int = u >> 2
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

