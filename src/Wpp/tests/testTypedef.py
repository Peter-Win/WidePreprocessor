import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTypedef(unittest.TestCase):
	def testSimple(self):
		source = """
typedef Value: double
		"""
		module = WppCore.createMemModule(source, 'typedef.fake')
		t = module.dictionary['Value']
		self.assertEqual(t.type, 'Typedef')
		self.assertEqual(t.name, 'Value')
		self.assertEqual(t.getAccessLevel(), 'public')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testInClass(self):
		source = """
class public Point
	typedef Value: double
		# Abstract value
	field x: Value
		"""
		module = WppCore.createMemModule(source, 'typedef.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
