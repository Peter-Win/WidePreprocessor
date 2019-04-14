from functools import reduce
from core.TaxonModule import TaxonModule
from Wpp.readWpp import readWpp
from Wpp.WppDictionary import WppDictionary

class WppModule(TaxonModule, WppDictionary):
	extension = '.wpp'
	# def __init__(self, name):
	# 	super().__init__()
	# 	self.name = name
	# 	self._accessTest = False

	def read(self, context):
		readWpp(context, self)

	def readBody(self, context):
		from Wpp.WppClass import WppClass
		from Wpp.WppInterface import WppInterface
		from Wpp.WppVar import WppVar
		from Wpp.WppFunc import WppFunc
		# from Wpp.WppTypedef import WppTypedef

		word = context.getFirstWord()
		if word == 'class':
			return WppClass()
		if word == 'interface':
			return WppInterface()
		if word == 'var':
		 	return WppVar()
		if word == 'func':
			return WppFunc()
		# if word == 'typedef':
		# 	return WppTypedef()
		return super().readBody(context)

	def addTaxon(self, taxon):
		if taxon.type == 'Func':
			taxon.addFuncToOwner(self)
			return taxon
		return super().addTaxon(taxon)

	def onUpdate(self):
		super().onUpdate()
		class SetAccess:
			def check(self):
				return True
			def exec(self):
				taxon = self.taxon
				if len(taxon.items) == 1:
					# Если в модуле всего один таксон, то он должен быть public
					item = taxon.items[0]
					access = item.getAccessLevel()
					if not access:
						item.attrs.add('public')
					elif access != 'public':
						item.throwError('Single item in module "%s" must be public' % (taxon.name,))
				else:
					# Необходимо не менее одного элемента модуля с доступом public
					publicCount = reduce(lambda acc, item: acc + (1 if item.getAccessLevel() == 'public' else 0), taxon.items, 0)
					if publicCount == 0:
						self.taxon.throwError('Not found public items in module "%s"' % (taxon.name,))
		self.addTask(SetAccess(), 'setAccess')
