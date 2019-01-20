import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTemplate(unittest.TestCase):
	@unittest.skip('Template not implemented yet')
	def testFunc(self):
		source = """
func template abs: @Value
	param x: @Value
	x < 0 ? -x : x

func public main
	var i: int = abs(-1)
	var x: double = abs(-4.5)
	var a: float = abs(1)
		"""
		module = WppCore.createMemModule(source, 'abs.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), '')