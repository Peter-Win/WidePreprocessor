import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppString(unittest.TestCase):
	def testRightOk(self):
		source = """
func public main
	var s: String = "Hello"
	var s2: String = s
	var s3: String
	s3 = s
	var firstL: int = s.find("l")
	var letter: String = s[1]
	s3 = s + "suffix"
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testWrongConst(self):
		source = """
func public main
	var s: String = 1
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "1:int" to "String"')

	def testWrongVar(self):
		""" float const can't be matched to string"""
		source = """
func public main
	var x: float = 1.1
	var s: String = x
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "x:float" to "String"')

	def testWrongVar(self):
		""" float variable can't be matched to string"""
		source = """
func public main
	var x: float = 1.1
	var s: String = x
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "x:float" to "String"')

	def testWrongIndex(self):
		"""Invalid index type"""
		source = """
func public main
	var s: String = "ABC"
	var c: String = s["0"]
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from ""0":string" to "unsigned long"')
