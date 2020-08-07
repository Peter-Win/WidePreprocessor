import unittest
from Wpp.WppCore import WppCore
from core.TaxonOverload import TaxonOverload
from core.TaxonAltName import TaxonAltName
from Wpp.WppExpression import WppConst
from core.ErrorTaxon import ErrorTaxon

def getAltName(taxon):
	return TaxonAltName.getAltName(taxon)

class TestWppOverload(unittest.TestCase):
	def testFindSuitablePure(self):
		source = """
func public overload hello
	altName twoInt
	param a: int
	param b: int

func public overload hello
	altName threeInt
	param a: int
	param b: int
	param c: int

func public overload hello
	altName twoLong
	param a: long
	param b: long
"""

		module = WppCore.createMemModule(source, 'findSuitablePure.wpp')
		hello = module.findItem('hello')
		self.assertEqual(hello.type, TaxonOverload.type)

		qtInt = module.core.findItem('int').buildQuasiType()
		qtLong = module.core.findItem('long').buildQuasiType()
		qtDouble = module.core.findItem('double').buildQuasiType()
		qtBool = module.core.findItem('bool').buildQuasiType()
		constInt = WppConst.create('1')
		qtConstInt = constInt.buildQuasiType()
		helloFuncs = hello.items

		# Если None присутствует в списке аргументов, значит результат будет None
		self.assertIsNone(TaxonOverload.findSuitablePure([None], helloFuncs))
		# Слишком много фактических параметров
		self.assertEqual(TaxonOverload.findSuitablePure([qtInt, qtInt, qtInt, qtInt, qtInt, qtInt], helloFuncs), 'NoSuitable')
		# Слишком мало фактических параметров
		self.assertEqual(TaxonOverload.findSuitablePure([qtInt], helloFuncs), 'NoSuitable')
		# Найти вариант с двумя int по строгому соответствию
		res = TaxonOverload.findSuitablePure([qtInt, qtInt], helloFuncs)
		self.assertEqual(res.type, 'func')
		self.assertEqual(getAltName(res), 'twoInt')
		# Вариант с двумя long по строгому соответствию
		res = TaxonOverload.findSuitablePure([qtLong, qtLong], helloFuncs)
		self.assertEqual(getAltName(res), 'twoLong')
		# Вариант с двумя long по нестрогому соответствию int, long
		res = TaxonOverload.findSuitablePure([qtInt, qtLong], helloFuncs)
		self.assertEqual(getAltName(res), 'twoLong')
		# Нет подходящего варианта для int, bool
		res = TaxonOverload.findSuitablePure([qtInt, qtBool], helloFuncs)
		self.assertEqual(res, 'NoSuitable')
		# Если один аргумент с точным типом, а второй получен из константы, то поиск удачный
		res = TaxonOverload.findSuitablePure([qtInt, qtConstInt], helloFuncs)
		self.assertEqual(getAltName(res), 'twoInt')
		# Если два аргумента константы, то им соответствуют оба варианта int, int и long, long. Это ошибка
		res = TaxonOverload.findSuitablePure([qtConstInt, qtConstInt], helloFuncs)
		self.assertEqual(res, 'NoSuitable')

	def testValidOverloads(self):
		source = """
func public overload hello: int
	altName helloInt
	param a: int
	param b: int

func public overload hello: long
	altName helloLong
	param a: long
	param b: long

var i: int = 0
var res11: int = hello(i, 1)
var res12: int = hello(i, res11)
var big: long = 0
var res21: long = hello(big, 21)
var res22: long = hello(big, res21)
"""
		module = WppCore.createMemModule(source, 'overloadOk.wpp')
		res11 = module.findItem('res11')
		expr11 = res11.getValueTaxon()
		self.assertEqual(expr11.type, 'call')
		self.assertEqual(expr11.getCaller().type, 'named')
		self.assertEqual(expr11.getCaller().getTarget().type, 'func')
		self.assertEqual(getAltName(expr11.getCaller().getTarget()), 'helloInt')

		self.assertEqual(getAltName(module.findItem('res12').getValueTaxon().getCaller().getTarget()), 'helloInt')
		self.assertEqual(getAltName(module.findItem('res21').getValueTaxon().getCaller().getTarget()), 'helloLong')
		self.assertEqual(getAltName(module.findItem('res22').getValueTaxon().getCaller().getTarget()), 'helloLong')


	def testInvalidConstants(self):
		""" We have 2 overloaded function for int and long. But call with constant arguments can't choose between these cases """
		source = """
func public overload hello: int
	altName helloInt
	param a: int
	param b: int

func public overload hello: long
	altName helloLong
	param a: long
	param b: long

var res: int = hello(11, 22)
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'invalidConst.wpp')
		self.assertEqual(cm.exception.args[0], 'No suitable func found for hello(11, 22)')


	def testInvalidType(self):
		""" We have 2 overloaded function for int and long. But call with constant arguments can't choose between these cases """
		source = """
func public overload hello: int
	altName helloInt
	param a: int
	param b: int

func public overload hello: long
	altName helloLong
	param a: long
	param b: long

var const i: int = 11
var res: int = hello(i, 22.2)
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'invalidType.wpp')
		self.assertEqual(cm.exception.args[0], 'No suitable func found for hello(int, 22.2)')
