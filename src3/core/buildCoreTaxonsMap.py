from core.TaxonRef import TaxonRef
from core.TaxonScalar import TaxonScalar
from core.TaxonTypedef import TaxonTypedef
from core.types.TaxonTypeExprName import TaxonTypeExprName

def buildCoreTaxonsMap():
	return {tx.type:tx for tx in [
		TaxonRef,
		TaxonScalar,
		TaxonTypedef,
		TaxonTypeExprName
	]}