from core.TaxonComment import TaxonComment

class WppComment(TaxonComment):
	def readHead(self, context):
		self.text = context.currentLine.strip()[1:]
		
	def export(self, outContext):
		outContext.writeln('#'+self.text)