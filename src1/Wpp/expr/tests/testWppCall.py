import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppCall(unittest.TestCase):
	def testCall(self):
		source = """
func myCalc: double
	param x: double
	param y: double

func public main
	var z: double = myCalc(1.234, 3)
		"""
		module = WppCore.createMemModule(source, 'fake.memory')
		ctx = OutContextMemoryStream()
		module.export()
		self.assertEqual(str(ctx), module.strPack(source))
