from core.TaxonFunc import TaxonOverloads, TaxonFunc, TaxonMethod, TaxonConstructor
from TS.TsTaxon import TsTaxon

class TsOverloads(TaxonOverloads):
	def __init__(self):
		super().__init__()
		self.phase = 0
	def onUpdate(self):
		res = super().onUpdate()
		self.phase += 1
		# Необходимо проверить наличие перегруженных функций. И если есть, то заменить на altName
		if self.phase == 2: # На первой фазе операторы расставляют свои altName
			if len(self.items) > 1:
				for fn in self.items:
					if not fn.altName:
						fn.throwError('Expected altname for overloaded function')
					fn.bUseAlt = True
					fn.prepareOverload()
		return res or self.phase < 2

	def export(self, outContext):
		if len(self.items) != 1:
			names = set()
			for item in self.items:
				name = item.getName(self)
				if name in names:
					self.throwError('TypeScript is not maintains overloaded function: %s(%s)' % (self.name, name))
				names.add(name)
		for item in self.items:
			item.export(outContext)

class TsCommonFunc(TsTaxon):
	def __init__(self):
		super().__init__()
		self.bUseAlt = False
	def exportSignature(self):
		""" Parameters + result type """
		s = '(' + ', '.join([p.exportString() for p in self.getParams()]) + ')'
		t = self.getResultType()
		if t:
			s += ': ' + t.exportString()
		return s

	def getName(self, user):
		return self.altName if self.bUseAlt else self.name

	def prepareOverload(self):
		pass

class TsFunc(TaxonFunc, TsCommonFunc):
	def export(self, outContext):
		s = 'function ' + self.getName(self)
		if self.getAccessLevel() == 'public':
			s = 'export ' + s
		s += self.exportSignature()
		s += ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')

class TsMethod(TaxonMethod, TsCommonFunc):
	def export(self, outContext):
		s = self.getAccessLevel() + ' '
		if 'static' in self.attrs:
			s += 'static '
		s += self.getName(self) + self.exportSignature() + ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')
		
class TsConstructor(TaxonConstructor, TsCommonFunc):
	def export(self, outContext):
		s = self.getAccessLevel();
		if self.bUseAlt:
			s += ' static function ' + self.altName
		else:
			s += ' constructor'
		s += self.exportSignature() + ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')

	def prepareOverload(self):
		self.instName = '_inst'
		body = self.getBody()

		# Создать экземпляр const _inst = new Type()
		clsTaxon = self.owner.owner
		varCmd = self.creator('Var')(name = self.instName)
		varCmd.attrs.add('const')
		locType = self.creator('TypeName')()
		locType.refs['type'] = clsTaxon
		value = self.creator('New')()
		clsName = self.creator('IdExpr')(clsTaxon.getName(self))
		clsName.refs['decl'] = clsTaxon
		value.addItem(clsName)
		varCmd.addItems([locType, value])
		body.addItem(varCmd, pos = 0)

		# Добавить return _inst
		ret = self.creator('Return')()
		retExpr = self.creator('IdExpr')(self.instName)
		retExpr.refs['decl'] = varCmd
		ret.addItem(retExpr)
		body.addItem(ret)

		# автоиниализация полей из параметров будет вставляться перед этой командой
		self.cmdAfterParamInit = body.items[1]
