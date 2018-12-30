from Taxon import Taxon

class WppTaxon(Taxon):
	""" Базовый класс для таксонов сообщества Wpp 
	Все таксоны сообщества должны уметь читать себя из wpp-описаний.
	Для этого есть три функции: readHead, readBody и addTaxon
	"""
	def readHead(self, context):
		pass
	def readBody(self, context):
		line = context.currentLine.strip()
		if line[0] == '#':
			self.addComment(line[1:])
			return None
		context.throwError('Invalid instruction')

	def addTaxon(self, taxon):
		return self.addItem(taxon)

	def exportComment(self, outContext):
		for line in self.getCommentLines():
			outContext.writeln('#' + line)