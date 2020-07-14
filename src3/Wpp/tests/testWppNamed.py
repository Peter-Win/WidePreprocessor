import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppNamed(unittest.TestCase):
	def testCommon(self):
		source = """
var const public a: int = 25
var public b: int = a
"""
		module = WppCore.createMemModule(source, 'common.wpp')
		out = OutContextMemoryStream()
		module.export(out)
		self.assertEqual(str(out), source.strip())