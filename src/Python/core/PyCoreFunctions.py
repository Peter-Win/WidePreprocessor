
def initFunctions(core):
	from Wpp.WppCore import WppCore
	src = """
func public len: unsigned long
	param s: String
"""

	srcModule = WppCore.createMemModule(src, 'pythonFunctions.core')
	dstModule = srcModule.cloneRoot(core)
	for taxon in dstModule.items:
		if taxon.getAccessLevel() == 'public':
			core.addNamedItem(taxon)

