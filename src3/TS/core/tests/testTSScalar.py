import unittest
from TS.core.TSScalar import TSScalar

class TestTSScalar(unittest.TestCase):
	def testNames(self):
		scalars = {props[0]:TSScalar(props) for props in TSScalar.propsList}
		scBool = scalars['bool']
		self.assertEqual(scBool.getName(), 'boolean')
		scInt = scalars['int']
		self.assertEqual(scInt.getName(), 'number')
		scDouble = scalars['double']
		self.assertEqual(scDouble.getName(), 'number')
