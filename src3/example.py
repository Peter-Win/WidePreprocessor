from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.TSCore import TSCore
from TS.style import style

source = """
func public fullCheck: double
	param a: double
	param b: double
	param c: double
	param d: double
	if a
		return a
	elif b
		return b
	elif c
		return c
	else
		return d
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

