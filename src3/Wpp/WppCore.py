from core.TaxonCore import TaxonCore
from Wpp.Context import Context

class WppCore(TaxonCore):
	def init(self):
		from Wpp.core.WppTaxonMap import WppTaxonMap
		self.taxonMap = WppTaxonMap
		super().init()

	def getDebugStr(self):
		return 'WppCore'

	reservedWords = ('Array', 'class', 'false', 'interface', 'Map', 'null', 'Set', 'this', 'true')

	def createRootModule(self, context):
		""" Создать корневой модуль
		Обычно приеняется для тестов. Т.к. полноценные проекты имеют корневой пакет.
		"""
		import os
		from Wpp.WppModule import WppModule
		nameExt = os.path.split(context.fileName)[1]
		name = os.path.splitext(nameExt)[0]
		module = self.setRoot(WppModule(name))
		module.read(context)
		module.initAll()
		self.resolveTasks()
		return module

	def createRootPackage(self, name, path):
		from Wpp.WppPackage import WppPackage
		srcRoot = self.setRoot(WppPackage(name))
		srcRoot.read(path)
		srcRoot.initAll()
		self.resolveTasks()
		return srcRoot

	@staticmethod
	def createMemModule(source, fakeName):
		core = WppCore.createInstance()
		return core.createRootModule(Context.createFromMemory(source, fakeName))
