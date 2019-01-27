from core.TaxonClass import TaxonClass
from TS.TsTaxon import TsTaxon

class TsMath(TaxonClass):
	def __init__(self):
		super().__init__()
		self.name = 'Math'
		for name in ['abs', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'exp', 'floor', 'log', 'log10', 'max', 'min', 'pow', 'round', 'sin', 'sqrt', 'tan']:
			self.addNamedItem(TsMathMethod(name = name))
		for name in ['PI', 'E']:
			self.addNamedItem(TsMathConst(name = name))
		self.addNamedItem(TsMathSqr(name = 'sqr'))
		self.addNamedItem(TsAngleCvt('degrees', '57.29577951308232'))
		self.addNamedItem(TsAngleCvt('radians', '0.017453292519943295'))

class TsMathMethod(TsTaxon):
	""" Функции, импортируемые из math """
	pass
class TsMathConst(TsTaxon):
	pass

class TsAngleCvt(TsTaxon):
	def __init__(self, name, coeff):
		super().__init__(name = name)
		self.coeff = coeff
	def onRef(self, user, key):
		pointBinOp = user.owner
		call = pointBinOp.owner
		arg = call.getArguments()[0]
		if arg.type != 'Const':
			mul = self.creator('BinOp')('*')
			mul.addItem(arg)
			mul.addItem(self.creator('Const')('fixed', self.coeff))
		else:
			# Небольшая оптимизация
			# TODO: желательно сделать общую функцию оптимизации, вычисляющая константы
			k = float(arg.value) * float(self.coeff)
			mul = self.creator('Const')('fixed', str(k))
		call.replace(mul)
		return True

class TsMathSqr(TsTaxon):
	type = 'MathSqr'
	def onRef(self, user, key):
		userOwner = user.owner
		if user.type == 'FieldExpr' and userOwner.type == 'BinOp':
			# Call
			# +--> BinOp(.)
			# |    +--> Math
			# |    +--> sqr
			# +--> arg
			callOwner = userOwner.owner
			if callOwner.type == 'Call':
				args = callOwner.getArguments()
				if len(args) == 1:
					newTaxon = self.creator('BinOp')()
					newTaxon.opCode = '**'
					newTaxon.addItem(args[0])
					newTaxon.addItem(self.creator('Const')('int', '2'))
					callOwner.replace(newTaxon)
					return True
