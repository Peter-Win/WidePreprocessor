import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestWppField(unittest.TestCase):

	def testStaticError(self):
		""" Invalid access to field from static member"""
		source = """
class public TestAbc
	field count: int = 123
	method static getCount: int
		return count
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'staticError.wpp')
		self.assertEqual(cm.exception.args[0], 'Non-static field "count" cannot be referenced from the static "getCount"')
