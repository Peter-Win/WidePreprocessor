from core.TaxonFunc import TaxonFunc
from Wpp.WppOverload import WppOverload

class WppFuncHelper:
	@staticmethod
	def checkDup(taxon, dup, context):
		if taxon.type == 'func' and taxon.isOverload() and dup.type == 'overload':
			return True
		""" Проверка дублирования имени. Необходимо встроить в функцию checkDup модуля или класса """
		if taxon.type == 'func' and dup.type in {'func', 'overload'}:
			context.throwError('Use "overload" attribute for "%s"' % (taxon.name))


	@staticmethod
	def addTaxon(owner, item, context):
		if not isinstance(item, TaxonFunc):
			return None
		if not item.isOverload():
			return None
		# Overload found
		overload = owner.findItem(item.name)
		if not overload:
			# первое вхождение перегруженной функции. требуется создать таксон управления перегрузкой
			overload = owner.addItem(WppOverload(item.name))
		overload.addItem(item)
		return overload
