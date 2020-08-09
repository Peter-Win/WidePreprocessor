from core.TaxonCore import TaxonCore

class PyCore(TaxonCore):
	def init(self):
		from Python.core.PyTaxonMap import PyTaxonMap
		self.taxonMap = PyTaxonMap
		super().init()

	def getDebugStr(self):
		return 'PythonCore'

	reservedWords = {
		'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
		'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
		'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
		'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
		'while', 'with', 'yield',
		'self', # Хотя self не является ключевым словом в питоне, но здесь оно зарезервировано в качестве this
	}

	@staticmethod
	def createModuleFromWpp(code, fileName):
		from Wpp.WppCore import WppCore
		wppModule = WppCore.createMemModule(code, fileName)
		return PyCore.createFromSource(wppModule)

	@staticmethod
	def createFromSource(src):
		pyCore = PyCore.createInstance()
		pyModule = pyCore.setRoot(src.cloneAll(pyCore))
		pyModule.initAllRefs()
		pyModule.initAll()
		pyCore.resolveTasks()
		return pyModule

