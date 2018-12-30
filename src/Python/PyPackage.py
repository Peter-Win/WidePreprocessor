from core.TaxonPackage import TaxonPackage

class PyPackage(TaxonPackage):
	def onNewFolder(self, outContext):
		# Создать пустой файл __init__.py в папке пакета
		f = outContext.createFile('__init__.py')
		f.close()
		