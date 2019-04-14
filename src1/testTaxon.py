import unittest
import os
from Taxon import Taxon
from core.ErrorTaxon import ErrorTaxon
from core.Ref import Ref

class MyTaxon(Taxon):
	def getItemNames(self):
		return ', '.join([item.name for item in self.items])

class TestTaxon(unittest.TestCase):
	def testThrowError(self):
		""" Тест генерации ошибки """
		taxon = Taxon()
		taxon._location = ('file.wpp', 22, 'Some text...')
		with self.assertRaises(ErrorTaxon) as cm:
			taxon.throwError('Hello')
		fileName, lineNumber, string = cm.exception.args[1]
		self.assertEqual(fileName, 'file.wpp')
		self.assertEqual(lineNumber, 22)
		self.assertEqual(string, 'Some text...')

	def testAddItem(self):
		""" Добавление подчиненных элементов """
		root = MyTaxon()
		first = root.addItem(Taxon('First'))
		self.assertEqual(root.getItemNames(), 'First')
		second = root.addItem(Taxon('Second'))
		self.assertEqual(root.getItemNames(), 'First, Second')
		zero = root.addItem(Taxon('Zero'), pos = 0)
		self.assertEqual(root.getItemNames(), 'Zero, First, Second')
		root.addItem(Taxon('1.5'), nextItem = second)
		self.assertEqual(root.getItemNames(), 'Zero, First, 1.5, Second')

	def testReplace(self):
		root = MyTaxon()
		second = Taxon('Second')
		root.addItems([Taxon('First'), second, Taxon('Third')]);
		self.assertEqual(root.getItemNames(), 'First, Second, Third')
		second.replace(Taxon('NewSecond'))
		self.assertEqual(root.getItemNames(), 'First, NewSecond, Third')

	def testGetClonedFields(self):
		def fieldsString(taxon):
			fields, refs = taxon.getClonedFields()
			v = list(fields)
			v.sort()
			r = list(refs)
			r.sort()
			return ', '.join(v), ', '.join(r)
		root = Taxon()
		self.assertEqual(fieldsString(root), ('_comment, _location, altName, name', ''))

		class SubTaxon(Taxon):
			__slots__ = ('x', 'y', 'z')
		taxon1 = SubTaxon()
		self.assertEqual(fieldsString(taxon1), ('_comment, _location, altName, name, x, y, z', ''))

		class DeepTaxon(SubTaxon):
			__slots__ = ('deep1', 'deep2', 'deep3')
			excludes = ('deep3')
		taxon2 = DeepTaxon();
		self.assertEqual(fieldsString(taxon2), ('_comment, _location, altName, deep1, deep2, name, x, y, z', ''))

		class Uber(DeepTaxon):
			pass
		taxon3 = Uber();
		self.assertEqual(fieldsString(taxon3), ('_comment, _location, altName, deep1, deep2, name, x, y, z', ''))

	def testGetPath(self):
		root = Taxon('root')
		trunk = Taxon('trunk')
		brunch = Taxon('brunch')
		leaf = Taxon('leaf')
		root.addItem(trunk)
		trunk.addItem(brunch)
		brunch.addItem(leaf)
		self.assertEqual(leaf.getPath(), 'root.trunk.brunch.leaf')

	def testGetAccessLevel(self):
		taxon = Taxon()
		taxon.attrs.add('public')
		self.assertEqual(taxon.getAccessLevel(), 'public')
		taxon = Taxon()
		taxon.attrs.add('private')
		self.assertEqual(taxon.getAccessLevel(), 'private')
		taxon = Taxon()
		taxon.attrs.add('protected')
		self.assertEqual(taxon.getAccessLevel('public'), 'protected')
		taxon = Taxon()
		self.assertEqual(taxon.getAccessLevel('public'), 'public')

	def testTasks(self):
		# Чтобы определить тип бинарного оператора, нужно взять типы подчиненных таксонов
		# Типы переменных получаются из объявлений
		core = Taxon()
		Taxon._queue = []
		class Type(Taxon):
			pass
		typeDict = {name:core.addItem(Type(name)) for name in ['int', 'float', 'string']}

		class SetType:
			def __init__(self, typeName, fieldName):
				self.typeName = typeName
				self.fieldName = fieldName
			def check(self):
				return True
			def exec(self):
				setattr(self.taxon, self.fieldName, typeDict[self.typeName])
			def __str__(self):
				return 'Type(%s -> %s)' % (self.typeName, self.fieldName)

		class VarDecl(Taxon):
			def __init__(self, name, typeName):
				super().__init__(name)
				self.typeName = typeName
				self.typeDecl = None
			def setup(self):
				self.addTask(SetType(self.typeName, 'typeDecl'), 'type')

		varList = [VarDecl('x', 'float'), VarDecl('i', 'int'), VarDecl('s', 'string')]
		varDict = {decl.name:core.addItem(decl) for decl in varList}

		class VarExpr(Taxon):
			def __init__(self, name):
				super().__init__(name)
				self.decl = None
				self.typeDecl = None
			def setDecl(self):
				class FindDecl:
					def check(self):
						return True
					def exec(self):
						self.taxon.decl = varDict[self.taxon.name]
					def __str__(self):
						return 'FindVar(%s)' % (self.taxon.name)
				self.addTask(FindDecl())
			def setType(self):
				class FindTypeV:
					def check(self):
						return self.taxon.decl and self.taxon.decl.typeDecl
					def exec(self):
						self.taxon.typeDecl = self.taxon.decl.typeDecl
					def __str__(self):
						return 'VarType(%s)' % (self.taxon.name)
				self.addTask(FindTypeV())
			def setup(self):
				self.setDecl()
				self.setType()

		class BinOpDecl(Taxon):
			def __init__(self, name, leftName, rightName, typeName):
				super().__init__(name)
				self.typeDecl = None
				self.typeName = typeName
				self.leftDecl = None
				self.leftName = leftName
				self.rightDecl = None
				self.rightName = rightName
			def setup(self):
				self.addTask(SetType(self.typeName, 'typeDecl'), 'type')
				self.addTask(SetType(self.leftName, 'leftDecl'), 'left')
				self.addTask(SetType(self.rightName, 'rightDecl'), 'right')

		binOps = [BinOpDecl('*', 'int', 'float', 'float'), BinOpDecl('+', 'string', 'int', 'string'), BinOpDecl('+', 'string', 'float', 'string')]
		for decl in binOps:
			core.addItem(decl).setup()

		class BinOpExpr(Taxon):
			def __init__(self, name, left, right):
				super().__init__(name)
				self.left = self.addItem(left)
				self.right = self.addItem(right)
				self.decl = None
				self.typeDecl = None
			def setup(self):
				class FindBinOp:
					def check(self):
						return self.taxon.left.typeDecl and self.taxon.right.typeDecl
					def exec(self):
						left = self.taxon.left.typeDecl
						right = self.taxon.right.typeDecl
						for binOp in binOps:
							if binOp.name == self.taxon.name and binOp.leftDecl == left and binOp.rightDecl == right:
								self.decl = binOp
								self.taxon.typeDecl = binOp.typeDecl
								return
						self.taxon.throwError('Not found declaration for ' + str(self))
					def __str__(self):
						return 'FindBinOp%s(%s, %s)' % (self.taxon.name, self.taxon.left.name, self.taxon.right.name)
				self.addTask(FindBinOp())


		expr = core.addItem(Taxon())
		# s + i * x
		i = VarExpr('i')
		x = VarExpr('x')
		s = VarExpr('s')
		op1 = BinOpExpr('*', i, x) # int + float
		op2 = expr.addItem(BinOpExpr('+', s, op1)) # s + i * x
		# Использование бинарных операторов начинается раньше, чем объявляются переменные
		for taxon in [op2, s, op1, i, x]: # Примерно в таком порядке осуществляется их обход в реальном выражении
			taxon.setup()
		for decl in varList:
			decl.setup()
		def queue2str():
			return ', '.join([str(task) for task in Taxon._queue])
		# Бинарный оператор оставляет FindBinOp, переменная - VarType
		self.assertEqual(queue2str(), 'FindBinOp+(s, *), VarType(s), FindBinOp*(i, x), VarType(i), VarType(x)')
		# Одна итерация
		status, newQueue = Taxon.resolveQueue(i._getQueue())
		i._setQueue(newQueue)
		# Выходят задачи поиска типа переменных, остаются задачи для бинопов
		self.assertEqual(queue2str(), 'FindBinOp+(s, *), FindBinOp*(i, x)')
		status, newQueue = Taxon.resolveQueue(i._getQueue())
		i._setQueue(newQueue)
		# Вычисляется тип для оператора *, остается +
		self.assertEqual(queue2str(), 'FindBinOp+(s, *)')
		status, newQueue = Taxon.resolveQueue(i._getQueue())
		i._setQueue(newQueue)
		# Теперь все задачи решены
		self.assertEqual(queue2str(), '')

	def testClone(self):
		class TaxonA(Taxon):
			type = 'NodeA'
			__slots__ = ('note')
			def __init__(self, name = ''):
				super().__init__(name)
				self.note = ''
		class TaxonB(Taxon):
			type = 'NodeB'
			__slots__ = ('lastItem', 'ref1')
			excludes = ('lastItem')
			refsList = ('ref1')
			def __init__(self, name = ''):
				super().__init__(name)
				self.special = None
				self.ref1 = None
			def onUpdate(self):
				class InitSpecial:
					def check(self):
						return True
					def exec(self):
						self.taxon.lastItem = self.taxon.owner.items[-1]
				self.addTask(InitSpecial())
		class DstCommon(Taxon):
			def __str__(self):
				arg = ', '.join([str(i) for i in self.items])
				res = self.name
				if arg:
					res += '(' + arg + ')'
				return res
		class SrcA(TaxonA):
			pass
		class SrcB(TaxonB):
			pass
		class SrcC(Taxon):
			type = 'NodeC'
		srcRoot = SrcA('A')
		srcRoot.note = 'Note A'
		srcB = SrcB('B')
		srcB.ref1 = Ref('TestFromB')
		srcRoot.addItems([srcB, SrcC('C')])
		# Исходное сообщество не поддерживает запись в строку
		class DstA(TaxonA, DstCommon):
			pass
		class DstB(TaxonB, DstCommon):
			pass
		class DstC(DstCommon):
			type = 'NodeC'
		class DstCore:
			taxonMap = {
				'NodeA': DstA,
				'NodeB': DstB,
				'NodeC': DstC,
			}
		# Клонирование
		dstRoot = srcRoot.cloneRoot(DstCore())
		self.assertEqual(str(dstRoot), 'A(B, C)')
		self.assertEqual(dstRoot.note, 'Note A')
		b, c = dstRoot.items
		self.assertEqual(b.lastItem, c) # Устанавливается в TaxonB.onUpdate > InitSpecial
		self.assertIs(type(b.ref1), Ref)
		self.assertEqual(b.ref1.name, 'TestFromB')

	def testIsMatch(self):
		class MyTaxon(Taxon):
			type = 'MyTaxon'
		class MyModule(Taxon):
			type = 'Module'
		taxon = MyTaxon('taxon')
		module = MyModule('module')
		self.assertTrue(taxon.isMatch({'name': 'taxon'}))
		self.assertFalse(module.isMatch({'name': 'module'}))
		self.assertFalse(taxon.isMatch({'name': 'taxon', 'isModule': True}))
		self.assertTrue(module.isMatch({'name': 'module', 'isModule': True}))

		def myCheck(taxon, params):
			return taxon.type == params['type'] and taxon.name == params['name']
		self.assertTrue(taxon.isMatch({'name': 'taxon', 'type': 'MyTaxon', 'cmp': myCheck}))
		self.assertFalse(taxon.isMatch({'name': 'taxon', 'type': 'Module', 'cmp': myCheck}))

	def testFindUp(self):
		# Проверка нескольких сценариев поиска
		# Есть два пакета, в каждом по два модуля. Каждый модуль содержит одноименный класс
		class MyPackage(Taxon):
			type = 'Package'
			def findUp(self, fromWho, params):
				if self.isMatch(params):
					return self
				# Пакет ищет среди всех подчиненных элементов, кроме того, откуда пришел запрос
				for item in self.items:
					if item != fromWho:
						result = self.findDown(params)
						if len(result) == 1:
							return result[0]
						if len(result) > 1:
							params['source'].throwError('Multiple definition of %s' % (params['name']))
				if self.owner:
					return self.owner.findUp(self, params)
			def findDown(self, params):
				return self._findDownRecursive(params)
		class MyModule(Taxon):
			type = 'Module'
			def findUp(self, fromWho, params):
				return self._findUpSiblings(fromWho, params)
			def findDown(self, params):
				if self.isMatch(params):
					return [self]
				# В настоящем модуле поиск возможен только среди public-элеменов
				return [item for item in self.items if item.isMatch(params)]
		class MyClass(Taxon):
			type = 'Class'
			def findUp(self, fromWho, params):
				return self._findUpSiblings(fromWho, params)
		root = MyPackage('root')
		package = root.addItem(MyPackage('package'))
		moduleA = root.addItem(MyModule('A'))
		moduleB = root.addItem(MyModule('B'))
		moduleC = package.addItem(MyModule('C'))
		moduleB1 = package.addItem(MyModule('B'))
		classA = moduleA.addItem(MyClass('A'))
		self.assertEqual(classA.getPath(), 'root.A.A')
		classB = moduleB.addItem(MyClass('B'))
		classC = moduleC.addItem(MyClass('C'))
		classB1 = moduleB1.addItem(MyClass('B'))
		varAx = classA.addItem(Taxon('x'))
		blockA = classA.addItem(Taxon('block'))
		exprA = blockA.addItem(Taxon('expr'))
		# Поиск ближайшего владельца - блока
		self.assertEqual(exprA.findUpEx('block'), blockA)
		# Поиск класса, которому принадлежит блок
		self.assertEqual(exprA.findUpEx('A'), classA)
		# Поиск переменной x, которая является частью класса А
		self.assertEqual(exprA.findUpEx('x').name, 'x')
		# Поиск модуля, которому принадлежит класс A
		self.assertEqual(exprA.findUp(exprA, {'name': 'A', 'isModule': True}), moduleA)
		# Поиск пакета, которому принадлежит модуль А
		self.assertEqual(exprA.findUpEx('root'), root)
		# Поиск класса B, должен вызвать ошибку, т.к есть root.B и root.package.B
		v = root.findDown({'name': 'B'})
		self.assertEqual(', '.join([i.getPath() for i in v]), 'root.package.B.B, root.B.B')
		with self.assertRaises(RuntimeError) as cm:
			self.assertEqual(exprA.findUpEx('B'), classB)
		self.assertEqual(str(cm.exception), '*Error* Multiple definition of B')
		# Поиск другого пакета
		self.assertEqual(exprA.findUpEx('package').name, 'package')
		# Поиск класса в другом пакете
		self.assertEqual(exprA.findUpEx('C'), classC)

	def testIsDeepContains(self):
		def create(owner, name):
			return owner.addItem(Taxon(name))
		root = Taxon('root')
		left = create(root, 'left')
		right = create(root, 'right')
		A = create(left, 'A')
		B = create(left, 'B')
		C = create(right, 'C')
		D = create(right, 'D')
		self.assertTrue(root.isDeepContains(left))
		self.assertFalse(left.isDeepContains(root))
		self.assertTrue(root.isDeepContains(A))
		self.assertTrue(left.isDeepContains(A))
		self.assertFalse(right.isDeepContains(A))
