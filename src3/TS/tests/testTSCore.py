import unittest
from TS.TSCore import TSCore

class TestTSCore(unittest.TestCase):
	def testReservedWords(self):
		core = TSCore.createInstance()
		self.assertEqual(core.getSafeName('myName'), 'myName')
		self.assertEqual(core.getSafeName('class'), 'class_')
		self.assertEqual(core.getSafeName('from'), 'from_')