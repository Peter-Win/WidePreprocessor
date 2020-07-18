from core.types.TaxonTypeExprName import TaxonTypeExprName
from core.TaxonRef import TaxonRef
from Wpp.WppTaxon import WppTaxon

class WppTypeExprName(TaxonTypeExprName, WppTaxon):
	""" Выражение, позволяющее найти тип по имени """
	__slots__ = ('typeName')

	def __init__(self):
		super().__init__()
		self.typeName = ''

	def onInit(self):
		# Нужно выполнить поиск типа по имени
		class TaskTypeFind:
			def check(self):
				return self.taxon.isCanFindUp()
			def exec(self):
				typeName = self.taxon.typeName
				txType = self.taxon.findUp(typeName, self)
				if not txType:
					self.taxon.throwError('Not found type "%s"' % typeName)
				if not txType.isType():
					self.taxon.throwError('"%s" is not a type' % typeName)
				# ссылка добавляется как подчиненный таксон выражения
				# self.taxon.addItem(TaxonRef.fromTaxon(txType))
				self.taxon.setType(txType)
		if not self.getTypeTaxon():
			self.addTask(TaskTypeFind())

	def exportString(self):
		words = self.getExportAttrs() + [self.typeName]
		return ' '.join(words)