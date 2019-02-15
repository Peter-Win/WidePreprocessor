import unittest
from Wpp.WppCore import WppCore
from Wpp.Context import Context
from out.OutContextMemory import OutContextMemory
from core.ErrorTaxon import ErrorTaxon

class TestWppBlock(unittest.TestCase):
	def testLocalVar(self):
		source = """
func localVar
	var tmp: int = 222
	var second: int = tmp + 1
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'localVar.fake'))
		over = module.dictionary['localVar']
		func = over.items[0]
		block = func.getBody()
		self.assertEqual(len(block.items), 2)
		cmd1 = block.items[0]
		self.assertEqual(cmd1.type, 'Var')

		outContext = OutContextMemory()
		cmd1.export(outContext)
		self.assertEqual(str(outContext), 'var tmp: int = 222')

		cmd2 = block.items[1]
		self.assertEqual(cmd2.type, 'Var')
		self.assertEqual(cmd2.name, 'second')
		val = cmd2.getValueTaxon()
		self.assertEqual(val.type, 'BinOp')
		varExpr = val.getLeft()
		self.assertEqual(varExpr.type, 'IdExpr')
		self.assertEqual(varExpr.id, 'tmp')
		self.assertEqual(varExpr.name, '')
		d1 = varExpr.getDeclaration()
		self.assertEqual(d1, cmd1)

	def testWrongLocalVar(self):
		source = """
func localVar
	var tmp: int = 222
	var second: int = tmp1 + 1
		"""
		core = WppCore()
		with self.assertRaises(ErrorTaxon) as ex:
			module = core.createRootModule(Context.createFromMemory(source, 'localVar.fake'))
		self.assertEqual(ex.exception.args[0], 'Name "tmp1" is not defined')
