from core.body.TaxonReturn import TaxonReturn
from Wpp.WppTaxon import WppTaxon
from Wpp.WppExpression import WppExpression
from core.TaxonFunc import TaxonFunc
from core.QuasiType import QuasiType

class WppReturn(TaxonReturn, WppTaxon):
	def readHead(self, context):
		exprCode = WppReturn.parse(context.currentLine)
		if exprCode:
			exprTaxon = WppExpression.parse(exprCode, context)
			self.setResult(exprTaxon)

	@staticmethod
	def parse(code):
		parts = code.split(' ', 1)
		if len(parts) == 1:
			return ''
		return parts[1].strip()

	def export(self, outContext):
		result = ['return']
		expr = self.getResult()
		if expr:
			result.append(expr.exportString())
		outContext.writeln(' '.join(result))

	def onInit(self):
		res = self.getResult()
		func = self.findOwnerByTypeEx(TaxonFunc)
		funcType = func.getResultTypeExpr()

		class TaskCheckType:
			def check(self):
				self.right = self.taxon.getResult().buildQuasiType()
				self.left = funcType.buildQuasiType()
				return self.left and self.right
			def exec(self):
				st, errMsg = QuasiType.matchTaxons(self.left, self.right)
				if errMsg:
					self.taxon.throwError(errMsg)

		if res:
			if not funcType:
				self.throwError('Expected return without expression')
			else:
				self.addTask(TaskCheckType())
		elif funcType:
			self.throwError('Expected return expression with type %s' % (funcType.exportString()))