import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTaxonId(unittest.TestCase):
	def testCheckShortStatic(self):
		source = """
class public MyClass
	field static inst: MyClass
	method static getInst: MyClass
		inst
	method setInst
		MyClass.inst = this
	method useInstShort: MyClass
		getInst()
	method useInstFull: MyClass
		MyClass.getInst()
		"""
		module = WppCore.createMemModule(source, 'MyClass.fake')
		myClass = module.dictionary['MyClass']
		useInstShort = myClass.dictionary['useInstShort'].items[0]
		cmd = useInstShort.getBody().items[0]
		self.assertEqual(cmd.type, 'Return')
		call = cmd.getExpression()
		self.assertEqual(call.type, 'Call')
		id = call.getCaller()
		self.assertEqual(id.type, 'IdExpr')
		res = id.checkShortStatic()
		self.assertEqual(res, myClass)

		useInstFull = myClass.dictionary['useInstFull'].items[0]
		cmd = useInstFull.getBody().items[0]
		self.assertEqual(cmd.type, 'Return')
		call = cmd.getExpression()
		self.assertEqual(call.type, 'Call')
		binOp = call.getCaller()
		self.assertEqual(binOp.type, 'BinOp')
		id = binOp.getLeft()
		self.assertEqual(id.type, 'IdExpr')
		res = id.checkShortStatic()
		self.assertIsNone(res)

	def testUpdateShortStatic(self):
		source = """
class public StClass
	field static inst: StClass
	method getInstShort: StClass
		inst
	method getInstFull: StClass
		StClass.inst
		"""
		expected = """
class public StClass
	field static inst: StClass
	method getInstShort: StClass
		StClass.inst
	method getInstFull: StClass
		StClass.inst
		"""
		module = WppCore.createMemModule(source, 'fake')
		stClass = module.dictionary['StClass']
		getInstShort = stClass.dictionary['getInstShort'].items[0]
		cmd = getInstShort.getBody().items[0]
		self.assertEqual(cmd.type, 'Return')
		exp = cmd.getExpression()
		self.assertEqual(exp.type, 'IdExpr')
		self.assertEqual(exp.checkShortStatic(), stClass)
		# Replace short form by full
		exp.updateShortStatic(stClass)

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
