import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppCall(unittest.TestCase):
	def testSimple(self):
		source = """
func public funcIf: double
	param cond: bool
	param positive: double
	param negative: double
	if cond
		return positive
	return negative

var const good: double = funcIf(true, 1.1, 3.3)

var const bad: double = funcIf(false, -1, -100)
"""
		module = WppCore.createMemModule(source, 'simpleCall.wpp')
		good = module.findItem('good')
		self.assertEqual(good.type, 'var')
		goodVal = good.getValueTaxon()
		self.assertEqual(goodVal.type, 'call')
		goodCallQT = goodVal.buildQuasiType()
		self.assertEqual(goodCallQT.type, 'scalar')
		self.assertEqual(goodCallQT.taxon.name, 'double')

		outCtx = OutContextMemoryStream()
		module.export(outCtx)
		self.assertEqual(str(outCtx), WppCore.strPack(source))

	def testToMuchArgs(self):
		source = """
func public func1: int
	param first: int
	return first

var result: int = func1(1, 2, 3)
"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'tooMuchArgs.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'func1() takes 1 argument but 3 were given')

	def testTooFewArgs(self):
		source = """
func public funcIf: double
	param cond: bool
	param positive: double
	param negative: double
	if cond
		return positive
	return negative
var result: double = funcIf(true)
"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'tooFewArgs.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'funcIf() missing required argument: "positive"')

	def testDefaultParam(self):
		source = """
func public funcIf: double
	param cond: bool
	param positive: double = 1
	param negative: double = -1
	if cond
		return positive
	return negative
var result: double = funcIf(true)
"""
		module = WppCore.createMemModule(source, 'defaultParam.wpp')
		outCtx = OutContextMemoryStream()
		module.export(outCtx)
		self.assertEqual(str(outCtx), WppCore.strPack(source))

	def testInvalidArgumentType(self):
		source = """
func public funcIf: double
	param cond: bool
	param positive: double
	param negative: double
	if cond
		return positive
	return negative

var const x: double = funcIf(1.1, 2.2, 3.3)
"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'invalidArg.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'Cannot convert from "fixed(1.1)" to "cond: bool"')
