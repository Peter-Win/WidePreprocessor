import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppInterface(unittest.TestCase):
	def testExport(self):
		source = """
interface public A
interface public B
	extends A
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInvalidParent(self):
		source = """
class public A
interface public B
	extends A
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Invalid parent root.A:Class')
