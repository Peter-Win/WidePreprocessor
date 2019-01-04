import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTernaryOp(unittest.TestCase):
	def testTernaryOp(self):
		source = """
func factorial: int
	param value: int
	value <= 1 ? 1 : factorial(value - 1) * value
		"""
		module = WppCore.createMemModule(source, 'factorial.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())