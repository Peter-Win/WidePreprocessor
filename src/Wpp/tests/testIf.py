import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestIf(unittest.TestCase):
	def testShort(self):
		source = """
func public simple: int
	param x: int
	if x < 0
		x = 0
	x
		"""
		module = WppCore.createMemModule(source, 'shortIf.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testElse(self):
		source = """
func public testElse: String
	param x: int
	var res: String
	if x < 0
		res = "Negative"
	else
		res = "Positive"
	res
		"""
		module = WppCore.createMemModule(source, 'testElse.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testPoly(self):
		source = """
func public testPoly
	param x: int
	var s: String
	if x == 0
		s = "Zero"
	elif x == 1
		s = "One"
	elif x == 2
		s = "Two"
	else
		s = "Else"
	s
		"""
		module = WppCore.createMemModule(source, 'testPoly.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
