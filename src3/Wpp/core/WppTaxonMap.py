from core.TaxonScalar import TaxonScalar
from Wpp.body.WppBody import WppBody
from Wpp.body.WppIf import WppIf
from Wpp.body.WppReturn import WppReturn
from Wpp.WppComment import WppComment
from Wpp.WppExpression import WppConst, WppNamed
from Wpp.WppFunc import WppFunc
from Wpp.WppModule import WppModule
from Wpp.WppTypedef import WppTypedef
from Wpp.WppVar import WppField, WppParam, WppVar
from Wpp.types.WppTypeExprName import WppTypeExprName

taxonsList = [
	TaxonScalar,
	WppBody,
	WppComment,
	WppConst,
	WppField,
	WppFunc,
	WppIf,
	WppModule,
	WppNamed,
	WppParam,
	WppReturn,
	WppTypedef,
	WppTypeExprName,
	WppVar,
]

WppTaxonMap = {taxon.type : taxon for taxon in taxonsList}
