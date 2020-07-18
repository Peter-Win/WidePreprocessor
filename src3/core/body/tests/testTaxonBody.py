import unittest
from Wpp.WppCore import WppCore

class TestTaxonBody(unittest.TestCase):
	def testFindUp(self):
		source = """
func public funcA
	var const first: bool = true
	var const second: int = 22
	var const third: double = 1.23
"""
		module = WppCore.createMemModule(source, 'findUp.wpp')
		funcA = module.findItem('funcA')
		body = funcA.getBody()
		self.assertEqual(len(body.items), 3)
		# Из второй строки можно найти первую
		res = body.items[1].getValueTaxon().startFindUp('first')
		self.assertEqual(res.name, 'first')
		# Из второй строки нельзя найти третью
		res = body.items[1].getValueTaxon().startFindUp('third')
		self.assertIsNone(res)
		# Из второй строки нельзя найти вторую. Потому что выражение используется раньше, чем будет объявлена переменная
		res = body.items[1].getValueTaxon().startFindUp('second')
		self.assertIsNone(res)
		# А из третьей можно найти вторую
		res = body.items[2].getValueTaxon().startFindUp('second')
		self.assertEqual(res.name, 'second')

