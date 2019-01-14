import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestForeach(unittest.TestCase):
	def testShort(self):
		source = """
func main
	var nums: Array int = [22, 33, 44]
	var sum: int = 0
	foreach nums => var value
		sum += value
		"""
		module = WppCore.createMemModule(source, 'foreachArray.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testFull(self):
		source = """
func main
	var nums: Array int = [22, 33, 44]
	var sum: int = 0
	foreach nums => var value => var i
		sum += value * (i + 1)
		"""
		module = WppCore.createMemModule(source, 'foreachFull.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testShortNoLocal(self):
		source = """
func main
	var nums: Array int = [22, 33, 44]
	var sum: int = 0
	var count: int
	foreach nums => count
		sum += count
		"""
		module = WppCore.createMemModule(source, 'foreachArray.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testFullNoLocal(self):
		source = """
func main
	var nums: Array double = [2.2, 3.3, 4.4]
	var result: double = 0
	var value: double
	var i: unsigned long
	foreach nums => value => i
		result += value * (i + 1)
		"""
		module = WppCore.createMemModule(source, 'foreachArray.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
