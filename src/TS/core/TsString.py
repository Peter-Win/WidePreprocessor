from TS.TsTaxon import TsTaxon
from TS.TsClass import TsClass

class TsString(TsClass):
	def __init__(self):
		super().__init__()
		self.name = 'String'

	def getName(self, user):
		if user.type == 'IdExpr' and user.owner.type == 'New':
			return 'String'
		return 'string'

	@staticmethod
	def exportConst(value):
		return '\'' + value + '\''