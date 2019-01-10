from Python.PyTaxon import PyTaxon
from Python.PyClass import PyClass

class PyStringLength(PyTaxon):
	type = 'StringLength'
	cloneScheme = 'Owner'
	def onRef(self, user, key):
		# Замена на функцию len
		userPt = user.owner
		assert(userPt.type == 'BinOp')
		assert(userPt.opCode == '.')
		assert(userPt.getRight() == user)

		lenExpr = self.core.taxonMap['IdExpr']()
		lenExpr.id = 'len'
		lenExpr.setRef('decl', self.core.dictionary['len'])
		lenCall = self.core.taxonMap['Call']()
		lenCall.addItems([lenExpr, userPt.getLeft()])
		userPt.replace(lenCall)

class PyString(PyClass):
	def __init__(self):
		super().__init__()
		self.name = 'String'
		self.addNamedItem(PyStringLength(name='length'))

	def getDefaultValue(self):
		return self.core.taxonMap['Const']('string', '""')

	@staticmethod
	def exportConst(value):
		return '"' + value + '"'