from Wpp.WppTaxon import WppTaxon
from core.TaxonModule import TaxonModule
from core.TaxonScalar import TaxonScalar
from core.Operators import StdBinOps
from Wpp.Context import Context
from Taxon import Taxon

class WppCore(TaxonModule):

	def __init__(self):
		super().__init__()
		from Wpp.core.WppTaxonMap import WppTaxonMap
		# from Wpp.core.WppString import WppString
		# from Wpp.core.WppArray import WppArray
		self.taxonMap = WppTaxonMap
		self.name = 'WppCore'

		for props in TaxonScalar.propsList:
			self.addNamedItem(WppTypeScalar(props))

		# complexTypes = [
		# 	('String', WppString),
		# 	('Array', WppArray)
		# ]
		# for name, Constructor in complexTypes:
		# 	inst = Constructor()
		# 	inst.name = name
		# 	self.addNamedItem(inst)
		# 	inst.init()
		# mathModule = self.createRootModule(Context.createFromMemory(Math, 'Math.fake'))
		# self.addNamedItem(mathModule.dictionary['Math'])



	def createRootModule(self, context):
		""" Создать корневой модуль
		Обычно приеняется для тестов. Т.к. полноценные проекты имеют корневой пакет.
		"""
		import os
		from Wpp.WppModule import WppModule
		nameExt = os.path.split(context.fileName)[1]
		name = os.path.splitext(nameExt)[0]
		module = WppModule(name)
		module.core = self
		module.owner = self
		module.read(context)
		module.fullUpdate()
		return module

	def createRootPackage(self, name, path):
		from Wpp.WppPackage import WppPackage
		srcRoot = WppPackage(name)
		srcRoot.core = self
		srcRoot.owner = self
		srcRoot.read(path)
		srcRoot.fullUpdate()
		return srcRoot

	@staticmethod
	def createMemModule(source, fakeName):
		core = WppCore()
		return core.createRootModule(Context.createFromMemory(source, fakeName))

class WppTypeScalar(TaxonScalar):
	pass

Math = """
class static Math
	field const PI: double = 3.141592653589793
		cloneScheme Owner
	field const E: double = 2.718281828459045
		cloneScheme Owner
	method pure abs: double
		cloneScheme Owner
		param value: double
	method pure max: double
		cloneScheme Owner
		param a: double
		param b: double
	method pure min: double
		cloneScheme Owner
		param a: double
		param b: double
	method pure sqr: double
		cloneScheme Owner
		param value: double
	method pure sqrt: double
		cloneScheme Owner
		param value: double
	method pure cos: double
		cloneScheme Owner
		param value: double
	method pure sin: double
		cloneScheme Owner
		param value: double
	method pure tan: double
		cloneScheme Owner
		param value: double
	method pure acos: double
		cloneScheme Owner
		param value: double
	method pure asin: double
		cloneScheme Owner
		param value: double
	method pure atan: double
		cloneScheme Owner
		param value: double
	method pure radians: double
		cloneScheme Owner
		param grad: double
	method pure degrees: double
		cloneScheme Owner
		param rad: double
	method pure round: double
		cloneScheme Owner
		param value: double
	method pure atan2: double
		cloneScheme Owner
		param y: double
		param x: double

"""