from Wpp.WppTaxon import WppTaxon
from core.TaxonModule import TaxonModule
from Wpp.Context import Context
from Taxon import Taxon

class WppCore(TaxonModule):

	def __init__(self):
		super().__init__()
		from Wpp.core.WppTaxonMap import WppTaxonMap
		from Wpp.core.WppString import WppString
		from Wpp.core.WppArray import WppArray
		self.taxonMap = WppTaxonMap
		self.name = 'WppCore'

		for name in Scalars:
			self.addNamedItem(WppTypeScalar(name))

		complexTypes = [
			('String', WppString),
			('Array', WppArray)
		]
		for name, Constructor in complexTypes:
			inst = Constructor()
			inst.name = name
			self.addNamedItem(inst)
			inst.init()


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


Scalars = [
	'bool',
	'int',
	'long',
	'float',
	'double'
]
class WppTypeScalar(Taxon):
	type = 'TypeScalar'
	def __init__(self, name):
		super().__init__()
		self.name = name
