from core.TaxonString import TaxonString
from Wpp.WppClass import WppClass
from Wpp.readWpp import readWpp
from Wpp.Context import Context

class WppString(TaxonString, WppClass):
	def init(self):
		content = """
field length: unsigned long
method find: int
	# return -1, if not found.
	param value: String
	param start: long = 0
	param end: long = -1
		# negative value used
method rfind: int
	param value: String
	param start: long = 0
	param end: long = -1
method upper: String
method lower: String
method slice: String
	param start: long = 0
	param end: long = -1
		"""
		# titem = self.addNamedItem(ArrayItemType(name='TItem'))
		# titem.attrs.add('public')
		ctx = Context.createFromMemory(content)
		readWpp(ctx, self)
