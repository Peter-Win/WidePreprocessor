from Taxon import Taxon

class TaxonCommonVar(Taxon):
	def getLocalType(self):
		return self.items[0]

	def getFinalType(self):
		return self.getLocalType().getFinalType()
	def getQuasiType(self):
		return self.getLocalType()	# TODO: Заменить на getFinalType
	def isQuasiReady(self):
		return self.getLocalType().isQuasiReady()

	def getValueTaxon(self):
		return self.items[1] if len(self.items) > 1 else None

	def getFieldDeclaration(self, name):
		return self.getLocalType().getFieldDeclaration(name)

	def autoInitField(self):
		""" Если это параметр конструктора, созданый через param init name, то возвращает поле name """
		return self.refs.get('field')

	def createParamInitCode(self):
		pt = self.creator('BinOp')(opCode = '.')
		pt.addItems([self.creator('This')(), self.creator('FieldExpr')(id = self.name)])
		pt.getRight().refs['decl'] = self.autoInitField()
		command = self.creator('BinOp')(opCode = '=')
		command.addItems([pt, self.creator('IdExpr')(id = self.name)])
		command.getRight().refs['decl'] = self;
		command.attrs.add('paramInitializer')
		return command

	def insertParamInitCode(self):
		"""
		Используется для параметров конструктора с атрибутом init.
		Генерирует код инициализации this.name = name
		Вызывается "вручную" из onUpdate таксона параметра для тех языков, где это нужно.
		А нужно почти всегда, кроме Wpp и С++. Ну или в TypeScript можно использовать constructor(public x: number)
		"""
		body = self.owner.getBody()
		body.addItem(self.createParamInitCode())

class TaxonVar(TaxonCommonVar):
	""" Классическая переменная.
	Обычно объявляется в блоке.
	Может быть объявлена в модуле, но только private.
	То есть, экспортировать переменные из модуля нельзя.
	"""
	type = 'Var'

class TaxonField(TaxonCommonVar):
	""" Поле - переменная класса """
	type = 'Field'
	canBeStatic = True

class TaxonReadonly(TaxonCommonVar):
	""" Поле, доступное только для чтения """
	type = 'Readonly'

class TaxonParam(TaxonCommonVar):
	""" Формальный параметр функции """
	type = 'Param'
