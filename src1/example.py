from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

source = """
func public main
	typedef TSize: unsigned long
	var a: TSize = 22.2
"""
module = WppCore.createMemModule(source, 'fake.memory')
outContext = OutContextMemoryStream()
module.export(outContext)
print(str(outContext))
