from Taxon import Taxon
from core.TaxonExpression import TaxonExpression
from core.body.TaxonBody import TaxonBody

# Возможна следующая конструкция:
# if expression1
# 	case1
# elif expression 2
# 	case2
# else
# 	case3
# В списке таксонов из нее получается
# 	expression1, case1, expression2, case2, case3

class TaxonIf(Taxon):
	type = 'if'
	
	def getStructure(self):
		"""
		Returns array of tuples: [('if', expression1, case1), ('elif', expression2, case2), ('else', None, case3)]
		"""
		cmd = 'if'
		expr = None
		body = None
		result = []
		for taxon in self.items:
			if isinstance(taxon, TaxonExpression):
				expr = taxon
			elif isinstance(taxon, TaxonBody):
				body = taxon
				if expr and body:
					result.append((cmd, expr, body))
					cmd = 'elif'
					expr = None
					body = None
		if body:
			result.append(('else', None, body))
		return result
