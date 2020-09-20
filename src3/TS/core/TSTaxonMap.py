from core.TaxonAltName import TaxonAltName
from core.TaxonOpDecl import TaxonDeclAssignBase
from core.TaxonRef import TaxonRef
from TS.body.TSBody import TSBody
from TS.body.TSIf import TSIf
from TS.body.TSReturn import TSReturn
from TS.core.TSScalar import TSScalar
from TS.TSClass import TSClass, TSExtends
from TS.TSComment import TSComment
from TS.TSExpression import TSConst, TSNamed, TSCall, TSNew, TSMemberAccess, TSBinOp, TSThis, TSSuper
from TS.TSFunc import TSConstructor, TSFunc, TSMethod
from TS.TSModule import TSModule
from TS.TSOverload import TSOverload
from TS.TSTypedef import TSTypedef
from TS.TSTypeExpr import TSTypeExprName
from TS.TSVar import TSAutoinit, TSField, TSVar, TSParam

TSTaxonList = [
	TaxonAltName,
	TaxonDeclAssignBase,
	TaxonRef,
	TSAutoinit,
	TSBinOp,
	TSBody,
	TSCall,
	TSComment,
	TSConst,
	TSConstructor,
	TSClass,
	TSExtends,
	TSField,
	TSFunc,
	TSIf,
	TSMemberAccess,
	TSMethod,
	TSModule,
	TSNamed,
	TSNew,
	TSOverload,
	TSParam,
	TSReturn,
	TSScalar,
	TSSuper,
	TSThis,
	TSTypedef,
	TSTypeExprName,
	TSVar,
]

TSTaxonMap = {taxon.type : taxon for taxon in TSTaxonList}