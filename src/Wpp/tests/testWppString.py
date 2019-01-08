import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppCore(unittest.TestCase):
	def testLength(self):
		source = """
func test: String
	param value: String
	value.length == 0 ? "Empty" : "Full"
		"""
		module = WppCore.createMemModule(source, 'length.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())