import unittest
from Wpp.body.WppIf import WppIf
from Wpp.body.WppBody import WppBody
from Wpp.body.WppReturn import WppReturn
from Wpp.WppExpression import WppExpression
from out.OutContextMemoryStream import OutContextMemoryStream
from Wpp.Context import Context
from Wpp.WppCore import WppCore

class TestWppIf(unittest.TestCase):
	def testExport(self):
		inCtx = Context.createFromMemory([''])
		txif = WppIf()
		txif.addItem(WppExpression.parse('first', inCtx))
		txBody = txif.addItem(WppBody())
		txRet = txBody.addItem(WppReturn())
		txRet.addItem(WppExpression.parse('1', inCtx))
		txif.addItem(WppExpression.parse('second', inCtx))
		txBody = txif.addItem(WppBody())
		txRet = txBody.addItem(WppReturn())
		txRet.addItem(WppExpression.parse('2', inCtx))
		txBody = txif.addItem(WppBody())
		txRet = txBody.addItem(WppReturn())
		txRet.addItem(WppExpression.parse('0', inCtx))
		outCtx = OutContextMemoryStream()
		txif.export(outCtx)
		expected = """
if first
	return 1
elif second
	return 2
else
	return 0
"""
		self.assertEqual(str(outCtx), expected.strip())

	def testFullStructure(self):
		source = """
func public fullCheck: double
	param a: double
	param b: double
	param c: double
	param d: double
	if a
		return a
	elif b
		return b
	elif c
		return c
	else
		return d
"""
		module = WppCore.createMemModule(source, 'fullif.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())

	def testShortStructure(self):
		source = """
func public fullCheck: double
	param cond: bool
	param positive: double
	param negative: double
	if cond
		return positive
	return negative
"""
		module = WppCore.createMemModule(source, 'shortif.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())

	def testElse(self):
		source = """
func public fullCheck: double
	param cond: bool
	param positive: double
	param negative: double
	if cond
		return positive
	else
		return negative
"""
		module = WppCore.createMemModule(source, 'else.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())
