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
		length = self.dictionary['length']
		length.cloneScheme = 'Owner'

	def matchQuasi(self, matchQuasi):
		if matchQuasi == self:
			return 'exact'
		if matchQuasi.type == 'Const':
			return 'constExact' if matchQuasi.constType == 'string' else ''
		return ''