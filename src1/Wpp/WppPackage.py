import os
from core.TaxonPackage import TaxonPackage
from Wpp.WppModule import WppModule
from Wpp.Context import Context


class WppPackage (TaxonPackage):
	def read(self, path):
		""" Рекурсивное чтение вложенных пакетов и модулей """
		for name in os.listdir(path):
			if name[0] == '.':
				continue
			fullName = os.path.join(path, name)
			splittedName = os.path.splitext(name)
			if os.path.isdir(fullName):
				# Если папка, то создать подчиненный пакет
				subPackage = self.addNamedItem(WppPackage(name))
				subPackage.read(fullName)
			elif splittedName[1] == '.wpp':
				# Если файл с расширением .wpp, то создать модуль
				module = self.addNamedItem(WppModule(splittedName[0]))
				ctx = Context.createFromFile(fullName)
				module.read(ctx)
