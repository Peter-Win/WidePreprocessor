import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestOperator(unittest.TestCase):
	def testMethod(self):
		source = """
class public Point
	field public x: double
	field public y: double
	operator +=: ref Point
		param pt: const ref Point
		x += pt.x
		y += pt.y
		this
		"""
		module = WppCore.createMemModule(source, 'method.fake')

		classPoint = module.dictionary['Point']
		self.assertEqual(classPoint.type, 'Class')
		opOver = classPoint.dictionary['+=']
		self.assertEqual(opOver.type, 'Overloads')
		self.assertEqual(opOver.name, '+=')
		op = opOver.items[0]
		self.assertEqual(op.type, 'Operator')
		self.assertEqual(op.name, '+=')
		self.assertTrue(op.isBinary())

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testUnary(self):
		source = """
class public Point
	field public x: double
	field public y: double
	constructor
		param init x
		param init y
	operator const -: ref Point
		Point(-x, -y)
		"""
		module = WppCore.createMemModule(source, 'methodUnary.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
