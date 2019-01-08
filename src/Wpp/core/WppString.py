from Wpp.WppClass import WppClass
from Wpp.Context import Context
from Wpp.readWpp import readWpp

class WppString(WppClass):
	def init(self):
		content = """
field length: unsigned long
		"""
		ctx = Context.createFromMemory(content)
		readWpp(ctx, self)