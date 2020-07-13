from Wpp.types.WppTypeExprName import WppTypeExprName
from Wpp.types.WppTypeExprArray import WppTypeExprArray

class WppTypeExpr:
	__slots__ = ()
	@staticmethod
	def parse(code, context):
		# Совсем простая реализация. Затычка
		words = code.split()
		if words[0] == 'Array':
			inst = WppTypeExprArray()
			itemExpr = ' '.join(words[1:])
			itemExprTaxon = WppTypeExpr.parse(itemExpr, context)
			inst.addItem(itemExprTaxon)
			return inst

		inst = WppTypeExprName()
		inst.typeName = words[-1]
		inst.attrs = set(words[0:-1])
		return inst