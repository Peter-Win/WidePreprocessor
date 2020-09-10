from Taxon import Taxon
from core.TaxonTypeExpr import TaxonTypeExpr
from core.TaxonExpression import TaxonExpression

class TaxonCommonVar(Taxon):
	def getTypeTaxon(self):
		# return self.items[0] if len(self.items) >= 1 else None
		return self.findByTypeEx(TaxonTypeExpr)

	def getValueTaxon(self):
		# return self.items[1] if len(self.items) >= 2 else None
		return self.findByTypeEx(TaxonExpression)

	def buildQuasiType(self):
		txType = self.getTypeTaxon()
		return txType.buildQuasiType() if txType else None

	def exportString(self):
		return '%s %s: %s' % (self.type, self.getName(), self.getTypeTaxon().exportString())


class TaxonVar(TaxonCommonVar):
	""" Классическая переменная.
	Обычно объявляется в блоке.
	Может быть объявлена в модуле, но только private.
	То есть, экспортировать переменные из модуля нельзя.
	"""
	type = 'var'

class TaxonField(TaxonCommonVar):
	""" Поле - переменная класса 
	attributes: static, public, private, protected
	"""
	type = 'field'
	canBeStatic = True

class TaxonReadonly(TaxonCommonVar):
	""" Поле, доступное только для чтения """
	type = 'readonly'

class TaxonParam(TaxonCommonVar):
	""" Формальный параметр функции
	"""
	type = 'param'

class TaxonAutoinit(TaxonCommonVar):
	""" 
	Автоматическая инициализация поля класса параметром конструктора
	                                                           TypeScript                         C++
	field myValue: SomeType          field myValue: SomeType   private myValue: SomeType;         private SomeType myValue;
	constructor                  <=> constructor               constructor(myValue: SomeType) {   MyClass(_myValue): myValue(_myValue) {}
	    param myValue: SomeType          autoinit myValue        this.myValue = myValue
	    this.myValue = myValue                                 }
	"""
	type = 'autoinit'

	def createStdImplementation(self):
		"""
		Standard implementation of autoinit: insert into body expression this.name = name
		Suitable languages: Python, TypeScript, PHP
		"""
		body = self.owner.getBody()
		pos = 0
		while pos < len(body.items) and 'autoinit' in body.items[pos].attrs:
			pos += 1
		eq = body.addItem(self.creator('binop')('='), pos)
		eq.attrs.add('instruction')
		eq.attrs.add('autoinit')
		left = eq.addItem(self.creator('dot')(self.getName()))
		left.addItem(self.creator('this')())
		right = eq.addItem(self.creator('named')(self.getName()))
		right.setTarget(self)
