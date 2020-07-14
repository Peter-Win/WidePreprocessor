from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.TSCore import TSCore
from TS.style import style

source = """
typedef public Size = unsigned long
var public const width: Size = 4
var const len: size_t = width
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

