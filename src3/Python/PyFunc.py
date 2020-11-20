from core.TaxonFunc import TaxonFunc, TaxonMethod, TaxonConstructor, TaxonOperator
from out.lexems import Lex
from Python.PyTaxon import PyTaxon
from utils.makeStaticConstructor import makeStaticConstructor

class PyCommonFunc(PyTaxon):
	def exportLexems(self, level, lexems, style):
		line = [Lex.keyword('def'), Lex.space, Lex.funcName(self.getName()), Lex.paramsBegin]

		paramLexems = []
		isStatic = False
		if self.owner.isClass() or (self.owner.type == 'overload' and self.owner.owner.isClass()):
			isStatic = self.isStatic()
			if not isStatic:
				paramLexems.append([Lex.keyword('self')])

		for param in self.getParamsList():
			pdef = []
			param.exportLexems(0, pdef, style)
			paramLexems.append(pdef)

		if len(paramLexems) > 0:
			for pl in paramLexems:
				line += pl
				line.append(Lex.paramDiv)
			line[-1] = Lex.paramDivLast

		line += [Lex.paramsEnd, Lex.colon]
		if isStatic:
			self.exportLine(level, lexems, style, [Lex.keyword('@staticmethod')])
		self.exportLine(level, lexems, style, line)

		self.exportInternalComment(level + 1, lexems, style)
		self.getBody().exportLexems(level + 1, lexems, style)

class PyFunc(TaxonFunc, PyCommonFunc):
	pass

class PyMethod(TaxonMethod, PyCommonFunc):
	pass

class PyOperator(TaxonOperator, PyCommonFunc):
	def getName(self):
		from core.operators import opcodeMap
		if 'useAltName' in self.attrs:
			return super().getName()

		decl = opcodeMap[self.getOpcode()]
		r = 'r' if 'right' in self.attrs else ''
		name = decl[1]
		if name == 'div':
			name = 'truediv'
		return '__%s%s__' % (r, name)

class PyConstructor(TaxonConstructor, PyCommonFunc):
	def isNeedRebuild(self):
		return 'overload' in self.attrs and len(self.getParamsList()) > 0

	def getName(self):
		if 'useAltName' in self.attrs:
			return super().getName()
		# if self.isNeedRebuild():
		# 	return '_' + TaxonAltName.getAltName(self)
		return '__init__'


	def onInit(self):
		if self.isNeedRebuild():
			# Нужно подождать, пока таксоны типа PyNamed выполнят замену field на self.field
			class TaskWait:
				def check(self):
					return True
				def exec(self):
					# self.taxon.rebuild()
					makeStaticConstructor(self.taxon)
			self.addTask(TaskWait())

	def rebuild(self):
		""" TODO: в дальнейшем можно оптимизировать. Чтобы сразу вызывать конструктор праметрами, которые полностью инициализируют объект.
		В Wpp запрещено объявлять дефолтные параметры в перегруженных функциях, но в питоне нет перегрузок. Поэтому возможен более оптимальный код:
		class simple Point                    class Point:
		  field x: double                       __slots__ = ('x', 'y')
		  field y: double                       def __init__(self, x = 0, y = 0):
		  constructor overload                    self.x = x
		    x = 0                                 self.y = y
		    y = 0                               @staticmethod
		  constructor overload                  def copyPoint(src):
		    altName initPoint                     return Point(src.x, src.y)
		    autoinit x
		    autoinit y
		  constructor overload                  Здесь удалось совместить два конструктора в одном за счет использования дефолтных параметров
		    altName copyPoint
		    param src: const ref Point
		    x = src.x
		    y = src.y
		"""
		# Check altName
		name = TaxonAltName.getAltName(self, 'overloaded constructor')
		self.attrs.add('useAltName')
		self.attrs.add('static')
		cls = self.findOwnerByType('class');
		body = self.getBody()
		instName = '_inst'
		inst = body.addItem(self.creator('var')(instName), 0)
		t = inst.addItem(self.creator('@typeExprName')())
		t.setType(cls)
		txNew = inst.addItem(self.creator('new')())
		caller = txNew.addItem(self.creator('named')(cls.getName()))
		caller.setTarget(cls)
		# Замена всех this на обращение к _inst
		def changeThis(taxon):
			if taxon.type == 'this':
				taxon.replaceTaxon(self.creator('named')(instName)).setTarget(inst)
		body.walk(changeThis)
		ret = body.addItem(self.creator('return')())
		retExpr = ret.addItem(self.creator('named')(instName))
		retExpr.setTarget(inst)
