import unittest
from Wpp.body.WppReturn import WppReturn
from Wpp.WppCore import WppCore

class TestWppReturn(unittest.TestCase):
	def testParse(self):
		self.assertEqual(WppReturn.parse(''), '')
		self.assertEqual(WppReturn.parse('return'), '')
		self.assertEqual(WppReturn.parse('return    '), '')
		self.assertEqual(WppReturn.parse('return hello'), 'hello')
		self.assertEqual(WppReturn.parse('return   hello'), 'hello')
		self.assertEqual(WppReturn.parse('return hello world'), 'hello world')

	def testEmpty(self):
		source = """
func public func1
	return
"""
		# В дальнейшем, пустая инструкция return может давать ошибку, если стоит в конце тела функции
		module = WppCore.createMemModule(source, 'emptyret.wpp')
		func1 = module.findItem('func1')
		self.assertEqual(func1.type, 'func')
		body = func1.getBody()
		self.assertEqual(len(body.items), 1)
		ret = body.items[0]
		self.assertEqual(ret.type, 'return')
		self.assertIsNone(ret.getResult())