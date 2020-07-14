from core.TaxonScalar import TaxonScalar
from Wpp.WppComment import WppComment
from Wpp.WppExpression import WppConst, WppNamed
from Wpp.WppModule import WppModule
from Wpp.WppTypedef import WppTypedef
from Wpp.WppVar import WppField, WppParam, WppVar
from Wpp.types.WppTypeExprName import WppTypeExprName

taxonsList = [
	TaxonScalar,
	WppComment,
	WppConst,
	WppField,
	WppModule,
	WppNamed,
	WppParam,
	WppTypedef,
	WppTypeExprName,
	WppVar,
]

WppTaxonMap = {taxon.type : taxon for taxon in taxonsList}
