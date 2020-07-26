from core.TaxonAltName import TaxonAltName
from core.TaxonRef import TaxonRef
from TS.body.TSBody import TSBody
from TS.body.TSIf import TSIf
from TS.body.TSReturn import TSReturn
from TS.core.TSScalar import TSScalar
from TS.TSComment import TSComment
from TS.TSExpression import TSConst, TSNamed
from TS.TSFunc import TSFunc
from TS.TSModule import TSModule
from TS.TSOverload import TSOverload
from TS.TSTypedef import TSTypedef
from TS.TSTypeExpr import TSTypeExprName
from TS.TSVar import TSVar, TSParam

TSTaxonList = [
	TaxonAltName,
	TaxonRef,
	TSBody,
	TSComment,
	TSConst,
	TSFunc,
	TSIf,
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