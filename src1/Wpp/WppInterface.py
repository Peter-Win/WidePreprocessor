from core.TaxonInterface import TaxonInterface
from core.Ref import Ref
from Wpp.WppDictionary import WppDictionary

class WppInterface(TaxonInterface, WppDictionary):
	def readHead(self, context):
		self._location = context.createLocation()
		words = context.currentLine.split()
		if len(words) < 2:
			self.throwError('Required interface name')
		self.name = words[-1]
		self.attrs = set(words[1:-1])
		# check attributes
		if 'protected' in self.attrs:
			context.throwError('Access level "private" cannot be applied to a interface')

	def readBody(self, context):
		word = context.getFirstWord()
		line = context.currentLine
		if word == 'extends':
			chunks = line.split()
			if len(chunks) != 2:
				context.throwError('Expected single name of class after "extends"')
			self.parent = Ref(chunks[1])
			return None
		return super().readBody(context)

	def onUpdate(self):
		result = super().onUpdate()
		# parent must be an Interface
		parent = self.getParent()
		if parent and parent.type != 'Interface':
			self.throwError('Invalid parent %s:%s' % (parent.getPath(), parent.type))
		return result

	def export(self, outContext):
		# head of class
		chunks = ['interface'] + self.getExportAttrs() + [self.name]
		outContext.writeln(' '.join(chunks))
		outContext.push()
		# comment
		self.exportComment(outContext)
		# extends
		parent = self.getParent()
		if parent:
			outContext.writeln('extends '+parent.getName(self))
		for item in self.items:
			item.export(outContext)
		outContext.pop()
