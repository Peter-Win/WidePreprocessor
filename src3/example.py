from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.TSCore import TSCore
from TS.style import style

source = """
func public overload hello: int
	altName helloInt
	param a: int
	param b: int

func public overload hello: long
	altName helloLong
	param a: long
	param b: long

var i: int = 0
var res11: int = hello(i, 1)
var res12: int = hello(i, res11)
var big: long = 0
var res21: long = hello(big, 21)
var res22: long = hello(big, res21)
"""

print('-- Wpp')
module = WppCore.createMemModule(source, 'example.wpp')
outCtx = OutContextMemoryStream()
module.export(outCtx);
print(str(outCtx))
print('')
print('-- TypeScript')
tsModule = TSCore.createFromSource(module)
outCtx = OutContextMemoryStream()
tsModule.exportContext(outCtx, style)
print(str(outCtx))

