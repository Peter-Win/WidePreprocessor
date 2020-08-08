import unittest
from Python.PyCore import PyCore
from Python.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyCore(unittest.TestCase):
	def testReservedWords(self):
		core = PyCore.createInstance()
		self.assertEqual(core.getSafeName('myName'), 'myName')
		self.assertEqual(core.getSafeName('class'), 'class_')
		self.assertEqual(core.getSafeName('from'), 'from_')
