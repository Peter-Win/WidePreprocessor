from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

source = """
func public main
	var a: Array String
	vas s: String = a[0][0]
"""
module = WppCore.createMemModule(source, 'fake.memory')
outContext = OutContextMemoryStream()
module.export(outContext)
print(str(outContext))
