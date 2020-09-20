from core.TaxonOpDecl import TaxonDeclAssignBase
from core.TaxonRef import TaxonRef
from core.TaxonScalar import TaxonScalar
from Wpp.body.WppBody import WppBody
from Wpp.body.WppIf import WppIf
from Wpp.body.WppReturn import WppReturn
from Wpp.WppAltName import WppAltName
from Wpp.WppComment import WppComment
from Wpp.WppClass import WppClass
from Wpp.WppExpression import WppConst, WppNamed, WppCall, WppSuper
from Wpp.WppExtends import WppExtends
from Wpp.WppFunc import WppFunc, WppMethod, WppConstructor
from Wpp.WppModule import WppModule
from Wpp.WppOverload import WppOverload
from Wpp.WppTypedef import WppTypedef
from Wpp.WppVar import WppAutoinit, WppField, WppParam, WppVar
from Wpp.types.WppTypeExprName import WppTypeExprName

taxonsList = [
	TaxonDeclAssignBase,
	TaxonRef,
	TaxonScalar,
	WppAltName,
	WppAutoinit,
	WppBody,
	WppCall,
	WppComment,
	WppConst,
	WppConstructor,
	WppClass,
	WppExtends,
	WppField,
	WppFunc,
	WppIf,
	WppMethod,
	WppModule,
	WppNamed,
	WppOverload,
	WppParam,
	WppReturn,
	WppSuper,
	WppTypedef,
	WppTypeExprName,
	WppVar,
]

WppTaxonMap = {taxon.type : taxon for taxon in taxonsList}
