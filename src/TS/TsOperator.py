from core.TaxonFunc import TaxonOperator
from TS.TsFunc import TsCommonFunc

class TsOperator(TaxonOperator, TsCommonFunc):
	def onUpdate(self):
		self.altName = self.getPossibleName()
		return super().onUpdate()

	def export(self, outContext):
		self.exportComment(outContext)
		name = self.getPossibleName()
		s = self.getAccessLevel() + ' ' + name
		s += self.exportSignature()
		s += ' {'
		outContext.writeln(s)
		self.getBody().export(outContext)
		outContext.writeln('}')