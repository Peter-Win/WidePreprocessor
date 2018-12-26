import unittest
from Wpp.Context import Context

class TestContext(unittest.TestCase):
	def testMemory(self):
		data = """
First line

	Second line

		Third line \
long
		"""
		ctx = Context.createFromMemory(data)
		line1 = ctx.readLine()
		self.assertEqual(line1, 'First line')
		self.assertEqual(ctx.getFirstWord(), 'First')
		self.assertFalse(ctx.isFinish())
		self.assertEqual(ctx.getCurrentLevel(), 0)
		line2 = ctx.readLine()
		self.assertEqual(line2, '\tSecond line')
		self.assertEqual(ctx.getCurrentLevel(), 1)
		line3 = ctx.readLine()
		self.assertEqual(line3, '\t\tThird line long')
		self.assertEqual(ctx.getCurrentLevel(), 2)
		line4 = ctx.readLine()
		self.assertEqual(line4, '')
		self.assertTrue(ctx.isFinish())