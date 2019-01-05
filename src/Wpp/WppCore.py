from Wpp.WppTaxon import WppTaxon
from core.TaxonModule import TaxonModule
from Wpp.Context import Context
from Taxon import Taxon

class WppCore(TaxonModule):

	def __init__(self):
		super().__init__()
		from Wpp.core.WppTaxonMap import WppTaxonMap
		self.taxonMap = WppTaxonMap
		self.name = 'WppCore'

		for name in Scalars:
			self.addNamedItem(WppTypeScalar(name))

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

	@staticmethod
	def createMemModule(source, fakeName):
		core = WppCore()
		return core.createRootModule(Context.createFromMemory(source, fakeName))


Scalars = [
	'int',
	'float',
	'double'
]
class WppTypeScalar(Taxon):
	type = 'TypeScalar'
	def __init__(self, name):
		super().__init__()
		self.name = name
