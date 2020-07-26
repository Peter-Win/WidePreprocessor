from core.TaxonAltName import TaxonAltName

class WppAltName(TaxonAltName):
	def readHead(self, context):
		words = context.currentLine.strip().split(' ')
		if len(words) != 2:
			context.throwError('Expected name in altName instruction')
		self.altName = words[1]

	def onInit(self):
		# Альтернативное имя должно быть уникально в пределах модуля
		module = self.findOwnerByType('module')
		if not module:
			self.throwError('Module not found')
		taxon = module.altNames.get(self.altName)
		if taxon:
			self.throwError('AltName "%s" already used by %s' % (self.altName, taxon.owner.getDebugStr()))
		module.altNames[self.altName] = self


	def export(self, outContext):
		outContext.writeln('%s %s' % (self.type, self.altName))