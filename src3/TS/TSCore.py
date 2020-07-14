from core.TaxonCore import TaxonCore

class TSCore(TaxonCore):
	def init(self):
		from TS.core.TSTaxonMap import TSTaxonMap
		self.taxonMap = TSTaxonMap
		super().init()

	def getDebugStr(self):
		return 'TSCore'

	reservedWords = ('break', 'case', 'catch', 'class', 'const', 'continue',
		'debugger', 'default', 'delete', 'do',
		'else', 'enum', 'export', 'extends', 'false', 'finally', 'for', 'function',
		'if', 'import', 'in', 'instanceof', 'new', 'null',
		'return', 'super', 'switch', 'this', 'throw', 'true', 'try', 'typeof',
		'var', 'void', 'while', 'with', 
		'as', 'implements', 'interface', 'let', 'package', 'private',
		'protected', 'public', 'static', 'yield',
		'any', 'boolean', 'constructor', 'declare', 'get', 'module', 'require',
		'number', 'set', 'string', 'symbol', 'type', 'from', 'of',
		)

	@staticmethod
	def createModuleFromWpp(code, fileName):
		from Wpp.WppCore import WppCore
		wppModule = WppCore.createMemModule(code, fileName)
		return TSCore.createFromSource(wppModule)

	@staticmethod
	def createFromSource(src):
		tsCore = TSCore.createInstance()
		tsModule = tsCore.setRoot(src.cloneAll(tsCore))
		tsModule.initAll()
		tsModule.initAllRefs()
		tsCore.resolveTasks()
		return tsModule

	aliasesMap = {
		'size_t': 'number',
		'byte': 'number',
		'uint8': 'number',
	}
