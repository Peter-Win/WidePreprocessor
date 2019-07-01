from core.TaxonClass import TaxonClass
from core.Ref import Ref
from Wpp.WppDictionary import WppDictionary

class WppClass(TaxonClass, WppDictionary):

	def readHead(self, context):
		self._location = context.createLocation()
		words = context.currentLine.split()
		if len(words) < 2:
			self.throwError('Required class name')
		self.name = words[-1]
		self.attrs = set(words[1:-1])
		# check attributes
		self.checkAttributes()
		self.checkAttributes(['abstract', 'static'])
		if 'protected' in self.attrs:
			context.throwError('Access level "protected" cannot be applied to a class')

	def readBody(self, context):
		from Wpp.WppVar import WppField, WppReadonly
		from Wpp.WppFunc import WppMethod, WppConstructor, WppOperator
		from Wpp.WppTypedef import WppTypedef
		# from Wpp.WppCast import WppCast
		word = context.getFirstWord()
		line = context.currentLine
		if word == 'extends':
			chunks = line.split()
			if len(chunks) != 2:
				context.throwError('Expected single name of class after "extends"')
			self.parent = Ref(chunks[1])
			return None
		if word == 'implements':
			chunks = line.split()
			self.implements = [Ref(name) for name in chunks[1:]]
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
		# if word == 'cast':
		# 	return WppCast()
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
		result = super().onUpdate()
		# parent must be a Class
		parent = self.getParent()
		if parent and parent.type != 'Class':
			self.throwError('Invalid parent %s:%s' % (parent.getPath(), parent.type))
		# implements - interfaces only!
		for i in self.implements:
			if i.target.type != 'Interface':
				self.throwError('Invalid interface %s:%s' % (i.target.getPath(), i.target.type))
		return result

	def export(self, outContext):
		# head of class
		chunks = ['class'] + self.getExportAttrs() + [self.name]
		outContext.writeln(' '.join(chunks))
		outContext.push()
		# comment
		self.exportComment(outContext)
		# extends
		parent = self.getParent()
		if parent:
			outContext.writeln('extends '+parent.getName(self))
		# implements
		if self.implements:
			outContext.writeln('implements ' + ' '.join([i.name for i in self.implements]))
		for item in self.items:
			item.export(outContext)
		outContext.pop()

	def validate(self, valueTaxon, attrs):
		""" Можно ли переменной данного класса присвоить указанное значение """
		if valueTaxon.type == 'Null':
			# Если класс объявлен с атрибутом simple, то null можно присваивать только указателю
			if 'simple' in self.attrs and 'ptr' not in attrs:
				return 'Cannot use null for simple class "%s" without pointer' % self.getName(self)
			return ''
		if valueTaxon.type == 'New' or valueTaxon.type == 'Call':
			sourceClass = valueTaxon.getCaller().getQuasiType()
			if sourceClass.canUpcastTo(self):
				return ''
		if valueTaxon.type == 'IdExpr':
			sourceClass = valueTaxon.getQuasiType()
			if sourceClass.canUpcastTo(self):
				return ''

		# self.throwError('Invalid value for class %s = %s:%s' % (self.name, valueTaxon.type, valueTaxon.exportString()))
		return 'NotFound'
