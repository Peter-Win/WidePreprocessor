from functools import reduce
from core.TaxonModule import TaxonModule
from Wpp.readWpp import readWpp
from Wpp.WppDictionary import WppDictionary

class WppModule(TaxonModule, WppDictionary):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self._accessTest = False

	def read(self, context):
		readWpp(context, self)

	def readBody(self, context):
		from Wpp.WppClass import WppClass
		from Wpp.WppVar import WppVar
		from Wpp.WppFunc import WppFunc

		word = context.getFirstWord()
		if word == 'class':
			return WppClass()
		if word == 'var':
			return WppVar()
		if word == 'func':
			return WppFunc()
		return super().readBody(context)

	def addTaxon(self, taxon):
		if taxon.type == 'Func':
			taxon.addFuncToOwner(self)
			return taxon
		return super().addTaxon(taxon)

	def onUpdate(self):
		if not self._accessTest:
			self._accessTest = True
			if len(self.items) == 1:
				# Если в модуле всего один таксон, то он должен быть public
				item = self.items[0]
				access = item.getAccessLevel()
				if not access:
					item.attrs.add('public')
				elif access != 'public':
					item.throwError('Single item in module must be public')
			else:
				# Необходимо не менее одного элемента модуля с доступом public
				publicCount = reduce(lambda acc, item: acc + (1 if item.getAccessLevel() == 'public' else 0), self.items, 0)
				if publicCount == 0:
					self.throwError('Not found public items in module "'+self.name+'"')


	def export(self, outContext):
		""" outContext типа OutContextFolder """
		writeContext = outContext.createFile(self.name + '.wpp')
		self.exportComment(outContext)
		for item in self.items:
			item.export(writeContext)
		writeContext.close()
