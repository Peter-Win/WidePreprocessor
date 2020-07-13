from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

source = """
typedef public Size = unsigned long
var public const width: Size = 4
var const len: size_t = width
"""

module = WppCore.createMemModule(source, 'example.wpp')
outCtx = OutContextMemoryStream()
module.export(outCtx);
print(str(outCtx))