import unittest
from Wpp.WppCore import WppCore
from core.ErrorTaxon import ErrorTaxon
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppFuncOverload(unittest.TestCase):
	def testOverloadErr(self):
		source = """
func public myFunc: double
	param val: double
	return val

func public myFunc: int
	param val: int
	return val
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'overloadErr.wpp')
		self.assertEqual(cm.exception.args[0], 'Use "overload" attribute for "myFunc"')

	def testOverloadOk(self):
		source = """
func overload public myFunc: double
	altName myFunc1
	param val: double
	return val

func overload public myFunc: int
	altName myFunc2
	param val: int
	return val
"""
		module = WppCore.createMemModule(source, 'overloadOk.wpp')
		over = module.findItem('myFunc')
		self.assertEqual(over.type, 'overload')
		self.assertEqual(len(over.items), 2)
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), WppCore.strPack(source))

		body = over.items[0].getBody()
		self.assertEqual(body.type, 'body')
		found = body.items[0].startFindUp('myFunc')
		self.assertEqual(found.type, 'overload')