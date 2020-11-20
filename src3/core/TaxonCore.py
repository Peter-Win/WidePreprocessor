from TaxonDict import TaxonDict
from core.TaxonScalar import TaxonScalar
from core.TaxonTypedef import TaxonTypedef
from core.types.TaxonTypeExprName import TaxonTypeExprName
from core.QuasiType import QuasiType
from core.TaxonOpDecl import TaxonDeclBinOp

class TaxonCore(TaxonDict):
	type = 'core'
	reservedWords = []

	@classmethod
	def createInstance(cls):
		inst = cls()
		inst.init()
		inst.initAll()
		inst.resolveTasks()
		return inst

	def __init__(self):
		super().__init__()
		self.tasks = []
		self.core = self
		self.root = None
		self.reservedWordsSet = {word for word in self.reservedWords}
		from core.buildCoreTaxonsMap import buildCoreTaxonsMap
		self.taxonMap = buildCoreTaxonsMap()
		self.binOpMap = {} # dictionary opcode => TaxonDeclBinOp[]
		self.priorMap = {} # opcode => priority

	def init(self):
		self.createScalar()
		self.createAliases()
		self.createPriorMap()
		self.createOperatorsDecl()

	def getSafeName(self, name):
		# Если имя совпало с одним из ключевых слов, то добавить подчерк в конце
		# Это гарантирует уникальность, т.к WPP запрещает использовать подчерки в именах, а в других языках это допустимо.
		return name if name not in self.reservedWordsSet else name + '_'

	def isReservedWord(self, word):
		return False

	def setRoot(self, root):
		self.root = self.addItem(root)
		return self.root

	def getRoot(self):
		return self.root

	def copyRootFrom(self, srcCore):
		""" Копирование проекта из другого сообщества """
		root = srcCore.getRoot().cloneAll(self)
		self.setRoot(root)
		root.initAllRefs()
		root.initAll()
		self.resolveTasks()

	def findByPathExt(self, pathExt):
		pos = 0
		currentTaxon = self
		if pathExt[0] == '@root':
			pos = 1
			currentTaxon = self.getRoot()
		while pos < len(pathExt):
			key = pathExt[pos]
			if type(key) == int:
				# Извлечь следующий таксон по индексу
				currentTaxon = currentTaxon.items[key]
			else:
				# В остальных случаях извлекается по имени
				currentTaxon = currentTaxon.findItem(key)
			pos += 1
		return currentTaxon

	def findUp(self, name, caller):
		""" Ядро ищет только среди непосредственно зарегистрированных по имени элементов.
		Если в ядре указанного имени нет, значит поиск закончился неудачно.
		"""
		return self.findItem(name)


	def addTaxonTask(self, taxon, task):
		self.tasks.append(task)
		task.taxon = taxon

	def resolveTasksIteration(self):
		""" Выполнить все задания в очереди 
		return (changed: bool, newQueue: Tasks[])
		"""
		changed = False
		newQueue = []
		# for task in queue:
		while self.tasks:
			task = self.tasks[0]
			if not task.taxon.isValid():
				changed = True # Таксон стал невалидным - исключить его из очереди
			elif task.check():
				task.exec()
				# Здесь в исходную очередь могут добавиться новые задания
				changed = True
			else:
				newQueue.append(task)
			self.tasks.pop(0)
		return (changed, newQueue)

	def resolveTasks(self):
		while len(self.tasks) > 0:
			changed, newQueue = self.resolveTasksIteration()
			if not changed:
				print(newQueue)
				self.throwError('Task list is not changed.')
			self.tasks = newQueue

	def createScalar(self):
		for props in TaxonScalar.propsList:
			inst = self.creator(TaxonScalar.type)(props)
			self.addItem(inst)

	def createAliases(self):
		from core.TaxonTypeAlias import TaxonTypeAlias
		for name, targetName, attrs in self.typeAliases:
			aliasName = self.aliasesMap[name] if self.aliasesMap else name
			tdef = TaxonTypeAlias(name, aliasName)
			self.addItem(tdef)
			tExpr = self.creator(TaxonTypeExprName.type)()
			tExpr.attrs = attrs
			tExpr.setType(self.findItem(targetName))
			tdef.setType(tExpr)

	typeAliases = [
		# size_t. Тип для описания целочисленных размеров. Например, длина массива. Заимствован из C++. Идентичен unsigned long
		('size_t', 'long', {'unsigned'}),
		('byte', 'int8', {'unsigned'}),
		('uint8', 'int8', {'unsigned'}),
	]
	aliasesMap = None

	# --------- Operators
	def createPriorMap(self):
		""" По-умолчанию используются приоритеты, указанные в списке операторов
		Они соответствуют: WPP, JavaScript, TypeScript
		"""
		from core.operators import opsList
		self.priorMap = {opcode:prior for opcode, name, opType, prior in opsList}


	def findBinOp(self, opcode, leftPart, rightPart):
		leftQType = leftPart.buildQuasiType()
		rightQType = rightPart.buildQuasiType()
		# Особый случай - оператор присваивания. Для дефольной реализации достаточно возможность привести правый тип к левому
		if opcode == '=':
			_, errMsg = QuasiType.matchTaxons(leftQType, rightQType)
			if errMsg:
				return None, errMsg
			return self.declAssignBase, None
		declList = self.binOpMap.get(opcode)
		if not declList:
			return None, 'Invalid operator %s' % opcode
		# Пока ищем первое попавшееся совпадение
		for decl in declList:
			leftResult, rightResult = decl.matchTypes(leftQType, rightQType)
			if leftResult and rightResult:
				return decl, None
		return None, 'Not found operator %s(%s, %s)' % (opcode, leftQType.getDebugStr(), rightQType.getDebugStr())

	def createOperatorsDecl(self):
		self.declAssignBase = self.addItem(self.creator('declAssignBase')())
		for opcode, left, right, result in binOps:
			decl = self.addItem(self.createDeclBinOp(opcode, opcode, self.mkQt(left), self.mkQt(right), self.mkQt(result)))
			opsList = self.binOpMap.setdefault(opcode, [])
			opsList.append(decl)

	def printOps(self):
		for id in self.binOpMap:
			print(id)
			opsList = self.binOpMap[id]
			for op in opsList:
				print('  ', op.name, '=>', op.opcode) 

	def mkQt(self, typeName):
		words = typeName.split()
		return QuasiType(self.findItem(words[-1]), set(words[0:-1]))

	def createDeclBinOp(self, originalOpcode, modifiedOpcode, qtLeft, qtRight, qtResult):
		return self.creator('declBinOp')(originalOpcode, modifiedOpcode, qtLeft, qtRight, qtResult)

arithOps = ['+', '-', '*', '/', '%']
arithAssigns = ['+=', '-=', '*=', '/=', '%=']
cmpOps = ['==', '!=', '<', '>', '<=', '>=']
logicalOps = ['|', '&', '^']
intTypes = ['int8', 'unsigned int8', 'short', 'unsigned short', 'int', 'unsigned int', 'long', 'unsigned long']
arithTypes = intTypes + [ 'float', 'double']
def _arithOpList(opcode):
	return [(opcode, t, t, t) for t in arithTypes] 
def _cmpOpList(opcode):
	return [(opcode, t, t, 'bool') for t in arithTypes]
def _arithAssignsList(opcode):
	return [(opcode, t, t, 'void') for t in arithTypes]
def _logicalList(opcode):
	return [(opcode, t, t, t) for t in intTypes]

# opcode, left, right, result
# сначала должны идти более специальные случаи, н.р. long + int8. т.к. иначе может сработать приведение типов, н.р. long + long
binOps = [
  ('&&', 'bool', 'bool', 'bool'),
  ('||', 'bool', 'bool', 'bool'),
  ('<<', 'int', 'unsigned int', 'int'),
  ('<<', 'unsigned int', 'unsigned int', 'unsigned int'),
  ('>>', 'int', 'unsigned int', 'int'),
  ('>>', 'unsigned int', 'unsigned int', 'unsigned int'),
  ('<<', 'long', 'unsigned long', 'long'),
  ('<<', 'unsigned long', 'unsigned long', 'unsigned long'),
  ('>>', 'long', 'unsigned long', 'long'),
  ('>>', 'unsigned long', 'unsigned long', 'unsigned long'),
]
for op in arithOps:
	binOps += _arithOpList(op)
for op in cmpOps:
	binOps += _cmpOpList(op)
for op in arithAssigns:
	binOps += _arithAssignsList(op)
for op in logicalOps:
	binOps += _logicalList(op)