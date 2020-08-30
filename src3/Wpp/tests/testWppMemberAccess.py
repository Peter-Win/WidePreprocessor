import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestMemberAccess(unittest.TestCase):
	def testThis(self):
		source = """
class A
	method getInstance: A
		return this
"""
		module = WppCore.createMemModule(source, 'this.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testField(self):
		source = """
class public Abc
	field value: double
	method const getValue: double
		return this.value
"""
		module = WppCore.createMemModule(source, 'field.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
