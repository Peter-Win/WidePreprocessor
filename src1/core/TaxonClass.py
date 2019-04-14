from core.TaxonWithParent import TaxonWithParent
from core.Ref import Ref

class TaxonClass (TaxonWithParent):
	type = 'Class'
	canBeStatic = True
	__slots__ = ('implements',)
	excludes = ('implements',)

	def __init__(self, name = ''):
		super().__init__(name)
		self.implements = []	# Array<Ref>

	def isClass(self):
		return True

	def isReady(self):
		for i in self.implements:
			if not i.isReady():
				return False
		return super().isReady()

	def isReadyFull(self):
		if not super().isReadyFull():
			return False
		for i in self.implements:
			if not i.isReady() or not i.target.isReadyFull():
				return False
		return True

	def getMembers(self):
		""" Члены класса в виде списка """
		return self.items

	def getMemberDeclaration(self, name):
		field = self.dictionary.get(name)
		if not field:
			self.throwError('Not found field "%s" in %s' % (name, self.getPath()))
		return field

	def _clone(self, newCore):
		newTaxon = super()._clone(newCore)
		newTaxon.implements = [i.clone() for i in self.implements]
		return newTaxon

	def onUpdate(self):
		super().onUpdate()
		for i in self.implements:
			i.find(self.owner)
		return True

	def findUp(self, fromWho, params):
		name = params['name']
		result = self.findWithParent(name)
		results = []
		if result:
			results.append(result)
		for i in self.implements:
			result = i.target.findWithParent(name)
			if result:
				results.append(result)
		if len(results) > 1:
			self.throwError('Multiple definition of "%s" in [%s]' % (name, ', '.join([r.getPath() for r in results])));
		if len(results) == 1:
			return results[0]
		return super().findUp(self, params)

	def findConstructor(self):
		from core.TaxonFunc import TaxonConstructor
		return self.dictionary.get(TaxonConstructor.key)

	def canUpcastTo(self, targetClass):
		result = super().canUpcastTo(targetClass)
		if not result:
			for iface in self.implements:
				if iface.target.canUpcastTo(targetClass):
					return True
		return result
