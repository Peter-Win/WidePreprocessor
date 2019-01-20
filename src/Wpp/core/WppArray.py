from Wpp.WppClass import WppClass
from Wpp.Context import Context
from Wpp.readWpp import readWpp

class WppArray(WppClass):
	def init(self):
		content = """
field length: unsigned long
	cloneScheme Owner
method push
	cloneScheme Owner
	param item: const ref @Item
		"""
		ctx = Context.createFromMemory(content)
		readWpp(ctx, self)
