import unittest
from Wpp.WppModule import WppModule
from Wpp.Context import Context
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppModule(unittest.TestCase):
	def testReadBody(self):
		ctx = Context.createFromMemory('class Hello')
		ctx.readLine()
		module = WppModule('test')
		result = module.readBody(ctx)
		self.assertIsNotNone(result)
		self.assertEqual(result.type, 'Class')

	def testRead(self):
		data = """
# Comment to module
class A
class B
		"""
		ctx = Context.createFromMemory(data, 'testRead.wpp')
		module = WppModule('test')
		module.read(ctx)
		self.assertIn('A', module.dictionary)
		self.assertIn('B', module.dictionary)
		self.assertEqual(module.getCommentLines(), [' Comment to module'])

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack("# Comment to module\nclass A\n\nclass B"))