from core.TaxonCast import TaxonCast
from TS.TsTaxon import TsTaxon

class TsCast(TaxonCast):
	def export(self, outContext):
		typeName = self.getSimpleName()
		methodName = ''
		if typeName == 'String':
			methodName = 'toString'
		if methodName:
			s = self.getAccessLevel() + ' ' + methodName + '(): '+self.getLocalType().exportString()+' {'
			outContext.writeln(s)
			self.getBody().export(outContext)
			outContext.writeln('}')
