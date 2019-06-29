"""
+------------------------
|   Call
+------------------------
| declTaxon <>--------------------> TaxonFunc
"""
from core.TaxonExpression import TaxonExpression
from core.QuasiType import QuasiType

class TaxonCall(TaxonExpression):
	type = 'Call'
	__slots__ = ('declTaxon')
	excludes = ('declTaxon',)
	def __init__(self):
		super().__init__()
		self.declTaxon = None # object
	def isReady(self):
		return self.declTaxon != None
	def isReadyFull(self):
		return self.isReady() and self.declTaxon.isReadyFull()

	def getCaller(self):
		return self.items[0]
	def getArguments(self):
		return self.items[1:]
	def exportString(self):
		s = self.priorExportString(self.getCaller()) + '('
		s += ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s
	def getDebugStr(self):
		return self.exportString()
	def buildQuasiType(self):
		if not self.declTaxon:
			self.throwError('%s not ready in buildQuasiType' % (self.type))
		return QuasiType.combine(self, self.declTaxon)

	def checkParams(self):
		""" Проверка соответствия типов формальных и фактических параметров """
		args = self.getArguments()
		formalParams = self.declTaxon.getParams()
		# Формальных параметров не может быть больше, чем фактических
		if len(args) > len(formalParams):
			self.throwError("Expected %d parameters instead of %d in %s %s" % (len(formalParams), len(args), self.type, self.getDebugStr()))
		# Проверить соответствие типов. Фактический должен кастоваться к формальному
		for i, arg in enumerate(args):
			formal = formalParams[i].buildQuasiType()
			formal.inst = self
			result, errMsg = QuasiType.matchTaxons(formal, arg)
			if not result:
				self.throwError('Invalid parameter #%d of %s: %s' % (i+1, self.declTaxon.getDebugStr(), errMsg))
		# Если фактических параметров меньше, чем формальных, то оставшиеся формальные должны иметь значение по-умолчанию
		i = len(args)
		while i < len(formalParams):
			formal = formalParams[i]
			i += 1
			if not formal.getValueTaxon():
				self.throwError('Expected parameter #%d (%s) in %s' % (i, formal.name, self.declTaxon.getDebugStr()))
	def _initDecl(self, decl):
		self.declTaxon = decl
		self.checkParams()

	def _setDecl(self, decl):
		class TaskCallOver:
			def __init__(self, over):
				self.over = over
			def check(self):
				return self.over.isReadyFull()
			def exec(self):
				taxon = self.taxon
				taxon._initDecl(self.over.find(taxon))
		if decl.type == 'Overloads':
			# TODO: Это может быть уже не актуально после поиска точной функции в onUpdate
			self.addTask(TaskCallOver(decl), 'over')
		elif decl.type == 'Method' or decl.type == 'Func':
			self._initDecl(decl)
		else:
			self.throwError('Invalid call declaration: ' + decl.type)


	def onUpdate(self):
		class TaskFindDecl:
			def check(self):
				self.decl = self.taxon.getCaller().getFuncDeclaration()
				return self.decl != None
			def exec(self):
				if self.decl.type == 'Overloads': # Найти подходящий вариант
					funcDecl = self.decl.find(self.taxon)
					self.decl = funcDecl
					
				self.taxon._setDecl(self.decl)
			def __str__(self):
				return 'TaxonCall.TaskFindDecl(%s:%s)' % (self.taxon.type, self.taxon.exportString())
		
		caller = self.getCaller()
		self.addTask(TaskFindDecl(), 'TaskFindDecl')
		return super().onUpdate()


class TaxonNew(TaxonCall):
	""" new Classname() """
	__slots__ = ()
	type = 'New'
