from core.TaxonClass import TaxonClass
from Wpp.WppDictionary import WppDictionary

class WppClass(TaxonClass, WppDictionary):
	__slots__ = ('_extends')
	def __init__(self):
		super().__init__()
		self._extends = None

	def getNameFor(self, user):
		""" Получить имя класса для указанного пользователя """
		#TODO: Пока просто имя. Но в будущем может понадобиться указывать уточняющий путь
		return self.name

	def readHead(self, context):
		self.location = context.createLocation()
		words = context.currentLine.split()
		if len(words) < 2:
			self.throwError('Required class name')
		self.name = words[-1]
		self.attrs = set(words[1:-1])
		# check attributes
		self.checkAttributes()
		self.checkAttributes(['static', 'abstract'])
		if 'protected' in self.attrs:
			context.throwError('Access level "private" cannot be applied to a class.')

	def readBody(self, context):
		from Wpp.WppVar import WppField, WppReadonly
		from Wpp.WppFunc import WppMethod, WppConstructor, WppOperator
		from Wpp.WppTypedef import WppTypedef
		from Wpp.WppCast import WppCast
		word = context.getFirstWord()
		line = context.currentLine
		if word == 'extends':
			chunks = line.split()
			if len(chunks) != 2:
				context.throwError('Expected single name of class after "extends"')
			self._extends = chunks[1]
			return None
		if word == 'field':
			return WppField()
		if word == 'readonly':
			return WppReadonly()
		if word == WppMethod.keyWord:
			return WppMethod()
		if word == WppConstructor.keyWord:
			return WppConstructor()
		if word == WppOperator.keyWord:
			return WppOperator(True)
		if word == 'typedef':
			return WppTypedef()
		if word == 'cast':
			return WppCast()
		return super().readBody(context)

	def addTaxon(self, taxon):
		if 'static' in self.attrs and taxon.canBeStatic:
			# Если класс статическмй, то элементы автоматически получают атрибут static
			taxon.attrs.add('static')
		if hasattr(taxon, 'classMember'):
			taxon.addFuncToOwner(self)
			return taxon
		return super().addTaxon(taxon)

	def onUpdate(self):
		if self._extends:
			# Нужно найти класс по имени и сформировать ссылку
			classDecl = self.findClassDeclaration(self._extends, True)
			if classDecl == self:
				self.throwError("Can't extends itself")
			self.setRef('ext', classDecl)
			self._extends = None
			# Для статического класса нужно добавить соответствующий атрибут во все подчиненные таксоны

	def export(self, outContext):
		# head of class
		chunks = ['class'] + list(self.attrs) + [self.name]
		outContext.writeln(' '.join(chunks))
		outContext.level += 1
		# comment
		self.exportComment(outContext)
		# extends
		parent = self.getParent()
		if parent:
			outContext.writeln('extends '+parent.getNameFor(self))
		for item in self.items:
			item.export(outContext)
		outContext.level -= 1
