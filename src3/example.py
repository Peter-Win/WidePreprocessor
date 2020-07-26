from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.TSCore import TSCore
from TS.style import style

source = """
func overload public dist: double
	altName dist2
	param x1: double
	param y: double
	return y
func overload public dist: double
	altName dist3
	param x: double
	param y: double
	param z: double
	return x
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

