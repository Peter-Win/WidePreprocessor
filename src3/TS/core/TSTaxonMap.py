from core.TaxonAltName import TaxonAltName
from core.TaxonRef import TaxonRef
from TS.body.TSBody import TSBody
from TS.body.TSIf import TSIf
from TS.body.TSReturn import TSReturn
from TS.core.TSScalar import TSScalar
from TS.TSClass import TSClass
from TS.TSComment import TSComment
from TS.TSExpression import TSConst, TSNamed, TSCall
from TS.TSFunc import TSFunc, TSMethod
from TS.TSModule import TSModule
from TS.TSOverload import TSOverload
from TS.TSTypedef import TSTypedef
from TS.TSTypeExpr import TSTypeExprName
from TS.TSVar import TSField, TSVar, TSParam

TSTaxonList = [
	TaxonAltName,
	TaxonRef,
	TSBody,
	TSCall,
	TSClass,
	TSComment,
	TSConst,
	TSField,
	TSFunc,
	TSIf,
	TSMethod,
	TSModule,
	TSNamed,
	TSOverload,
	TSParam,
	TSReturn,
	TSScalar,
	TSTypedef,
	TSTypeExprName,
	TSVar,
]

TSTaxonMap = {taxon.type : taxon for taxon in TSTaxonList}