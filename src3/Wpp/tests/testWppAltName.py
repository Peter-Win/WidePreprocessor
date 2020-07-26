import unittest
from Wpp.WppCore import WppCore
from core.TaxonAltName import TaxonAltName
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppAltName(unittest.TestCase):
	def testFunc(self):
		source = """
func public func1
	altName first
	return

func public func2: int
	altName second
	param a: int
	return a
"""
		module = WppCore.createMemModule(source, 'func.wpp')
		func1 = module.findItem('func1')
		self.assertEqual(func1.type, 'func')
		self.assertEqual(func1.getName(), 'func1')
		self.assertEqual(TaxonAltName.getAltName(func1), 'first')

		func2 = module.findItem('func2')
		self.assertEqual(func2.type, 'func')
		self.assertEqual(func2.getName(), 'func2')
		self.assertEqual(TaxonAltName.getAltName(func2), 'second')

		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), WppCore.strPack(source))

	def testDublicate(self):
		source = """
func proc1
	altName hello
func proc2
	altName hello
"""
		with self.assertRaises(RuntimeError) as cm:		
			module = WppCore.createMemModule(source, 'dup.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'AltName "hello" already used by func dup.proc1')
