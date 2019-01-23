import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestCast(unittest.TestCase):
	def testString(self):
		source = """
class public A
	field public s: String
	cast: String
		s 
		"""
		module = WppCore.createMemModule(source, 'A.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())