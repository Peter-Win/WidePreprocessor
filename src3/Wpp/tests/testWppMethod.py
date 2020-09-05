import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestWppMethod(unittest.TestCase):
	def testWrongOverload(self):
		source = """
class Value
	field x: double = 0
	method add: double
		param value: double
		return x + value
	method add: double
		param v: Value
		return x + v.x
"""
		with self.assertRaises(RuntimeError) as cm:		
			module = WppCore.createMemModule(source, 'wrongOverload.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'Use "overload" attribute for "add"')


	def testOverload(self):
		source = """
class Value
	field x: double = 0
	method overload add: double
		param value: double
		return x + value
	method overload add: double
		param v: Value
		return x + v.x
"""
		module = WppCore.createMemModule(source, 'overload.wpp')
		Value = module.findItem('Value')
		add = Value.findItem('add')
		self.assertEqual(add.type, 'overload')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
