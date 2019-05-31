from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

source = """
class public Atom
	readonly N: int
	readonly mass: double
	constructor
		param init N
		param init mass
func public main
	var H: Atom = Atom(1, 1.008)
	var waterMass: double = H.mass * 2
"""
	# var O: Atom = Atom(8, 15.999)
	# var waterMass: double = H.mass * 2 + O.mass


module = WppCore.createMemModule(source, 'fake.memory')
outContext = OutContextMemoryStream()
module.export(outContext)
print(str(outContext))

