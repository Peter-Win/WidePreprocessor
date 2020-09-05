from core.TaxonFunc import TaxonFunc
from Wpp.WppOverload import WppOverload

class WppFuncHelper:
	@staticmethod
	def checkDup(taxon, dup, context):
		if isinstance(taxon, TaxonFunc) and taxon.isOverload() and dup.type == 'overload':
			return True
		""" Проверка дублирования имени. Необходимо встроить в функцию checkDup модуля или класса """
		if isinstance(taxon, TaxonFunc) and dup.type in {'func', 'method', 'overload'}:
			context.throwError('Use "overload" attribute for "%s"' % (taxon.name))


	@staticmethod
	def addTaxon(owner, item, context):
		if not isinstance(item, TaxonFunc):
			return None
		if not item.isOverload():
			return None
		# Overload found
		if item.type == 'constructor':
			# Перегруженый конструктор
			con = owner.findConstructor()
			if not con:
				con = owner.addItem(WppOverload())
				con.attrs.add('constructor')
			con.addItem(item)
			return con

		overload = owner.findItem(item.name)
		if not overload:
			# первое вхождение перегруженной функции. требуется создать таксон управления перегрузкой
			overload = owner.addItem(WppOverload(item.name))
		overload.addItem(item)
		return overload
