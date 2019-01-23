from Taxon import Taxon

class TaxonExpression(Taxon):
	__slots__ = ('prior')
	def __init__(self):
		super().__init__()
		self.prior = 0

	def priorExportString(self, expr):
		s = expr.exportString()
		if self.prior < expr.prior:
			s = '(' + s + ')'
		return s

	def getDebugStr(self):
		return self.type

	def export(self, outContext):
		""" Используется в блоках. Например this.a = a """
		outContext.writeln(self.exportString())

class TaxonConst(TaxonExpression):
	type = 'Const'
	def __init__(self, constType = None, value = None):
		super().__init__()
		self.constType = constType
		self.value = value

	def clone(self, newCore):
		result = super().clone(newCore)
		result.constType = self.constType
		result.value = self.value
		return result

	def getDebugStr(self):
		return '%s(%s)' % (self.constType, self.value)

class TaxonNull(TaxonExpression):
	type = 'Null'

class TaxonTrue(TaxonExpression):
	type = 'True'

class TaxonFalse(TaxonExpression):
	type = 'False'

class TaxonId(TaxonExpression):
	__slots__ = ('id') # Идентификатор хранится не в name, чтобы при поиске findUp не происходило ложное срабатывание
	def clone(self, newCore):
		result = super().clone(newCore)
		result.id = self.id
		return result
	def getDeclaration(self):
		return self.refs['decl']
	def getFieldDeclaration(self, name):
		decl = self.getDeclaration()
		return decl.getFieldDeclaration(name)
	def getDebugStr(self):
		return self.id
	def checkShortStatic(self):
		""" Проверяет, является ли данная конструкция обращением к статическому члему класса без указания класса
		В Wpp такое возможно, но лишь внутри класса. В других языках нужно дописывать класс.
		Если нет, возвращает None. Если да - таксон того класса, которому принадлежит поле
		"""
		decl = self.getDeclaration()
		if decl.type == 'Class':
			return None
		if 'static' not in decl.attrs:
			return None
		ownerClass = decl.findOwner('Class')
		if not ownerClass:
			return None
		# Теперь надо проверить, не является ли правой частью частью бинарного оператора ClassName.member
		owner = self.owner
		if owner.type == 'BinOp' and owner.opCode == '.' and self == owner.getRight():
			leftDecl = owner.getLeft().getDeclaration()
			if leftDecl.type == 'Class':
				return None
		return ownerClass

	def updateShortStatic(self, classTaxon):
		""" Дописать имя класса к обращению к статическому члену. Вызывается из onUpdate если testShortStatic() вернет True """
		binOp = self.core.taxonMap['BinOp']()
		binOp.opCode = '.'
		self.replace(binOp)
		idClass = self.core.taxonMap['IdExpr']()
		field = self.core.taxonMap['FieldExpr']()
		binOp.addItems([idClass, field])
		idClass.id = classTaxon.name
		idClass.setRef('decl', classTaxon)
		field.id = self.id

class TaxonIdExpr(TaxonId):
	type = 'IdExpr'

class TaxonFieldExpr(TaxonId):
	type = 'FieldExpr'

class TaxonOpCode(TaxonExpression):
	__slots__ = ('opCode')
	def clone(self, newCore):
		result = super().clone(newCore)
		result.opCode = self.opCode
		return result

class TaxonUnOp(TaxonOpCode):
	type = 'UnOp'
	def getArgument(self):
		return self.items[0]
	def getDebugStr(self):
		return '(%s %s)' % (self.opCode, self.getArgument())

class TaxonBinOp(TaxonOpCode):
	type = 'BinOp'
	def getLeft(self):
		return self.items[0]
	def getRight(self):
		return self.items[1]
	def getDebugStr(self):
		return '(%s %s %s)' % (self.getLeft().getDebugStr(), self.opCode, self.getRight().getDebugStr())

class TaxonClassRef(TaxonExpression):
	def getClass(self):
		return self.findOwner('Class', True)
	def getFieldDeclaration(self, name):
		myClass = self.getClass()
		return myClass.getFieldDeclaration(name)

class TaxonThis(TaxonClassRef):
	type = 'This'

class TaxonSuper(TaxonClassRef):
	type = 'Super'

class TaxonCall(TaxonExpression):
	type = 'Call'
	def getCaller(self):
		return self.items[0]
	def getArguments(self):
		return self.items[1:]
	def exportString(self):
		s = self.priorExportString(self.getCaller()) + '('
		s += ', '.join([arg.exportString() for arg in self.getArguments()]) + ')'
		return s

class TaxonNew(TaxonCall):
	""" new Classname() """
	type = 'New'

class TaxonTernaryOp(TaxonExpression):
	type = 'TernaryOp'
	def getCondition(self):
		return self.items[0]
	def getPositive(self):
		return self.items[1]
	def getNegative(self):
		return self.items[2]

class TaxonArrayIndex(TaxonExpression):
	type = 'ArrayIndex'

class TaxonArrayValue(TaxonExpression):
	""" example: [1, 2, 3] """
	type = 'ArrayValue'
	def exportString(self):
		return '[' + ', '.join([i.exportString() for i in self.items]) + ']'
