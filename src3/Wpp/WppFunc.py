from core.TaxonFunc import TaxonFunc
from Wpp.WppTaxon import WppTaxon

class WppFunc(TaxonFunc, WppTaxon):
	@staticmethod
	def parseHead(code):
		""" return errMsg, name, attrs, resultType """
		pair = code.split(':', 1)
		nameAndAttrs = pair[0]
		resultType = pair[1].strip() if len(pair) == 2 else None
		words = nameAndAttrs.split()
		if len(words) < 2:
			return ('Expected name of ' + words[0], None, None, None)
		name = words[-1]
		attrs = set(words[1:-1])
		return (None, name, attrs, resultType)

