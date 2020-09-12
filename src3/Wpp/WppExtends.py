from core.TaxonExtends import TaxonExtends

class WppExtends(TaxonExtends):
	__slots__ = ('parentName')
	def __init__(self):
		super().__init__()
		self.parentName = ''

	def readHead(self, context):
		words = context.currentLine.split()
		if len(words) < 2:
			context.throwError('Expected name of parent class')
		if len(words) > 2:
			context.throwError('Too many names. Expected one name of parent class')
		self.parentName = words[1]

	def onInit(self):
		currentClass = self.owner
		parentClass = currentClass.owner.startFindUp(self.parentName)
		if not parentClass:
			self.throwError('Parent class not found: %s' % self.parentName)
		if not parentClass.isClass():
			self.throwError('Expected parent class "%s", but %s found' % (self.parentName, parentClass.type))
		self.setParent(parentClass)

	def export(self, outContext):
		outContext.writeln('extends %s' % self.getParent().getName())
