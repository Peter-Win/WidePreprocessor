import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPyClass(unittest.TestCase):
	def testExtends(self):
		source = """
class Top
class Middle
	extends Top
class Bottom
	extends Middle
"""
		expect = """
class Top:
	pass
class Middle(Top):
	pass
class Bottom(Middle):
	pass
"""
		module = PyCore.createModuleFromWpp(source, 'extends.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expect))
