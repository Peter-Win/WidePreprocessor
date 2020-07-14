from core.TaxonRef import TaxonRef
from TS.core.TSScalar import TSScalar
from TS.TSComment import TSComment
from TS.TSExpression import TSConst, TSNamed
from TS.TSModule import TSModule
from TS.TSTypedef import TSTypedef
from TS.TSTypeExpr import TSTypeExprName
from TS.TSVar import TSVar

TSTaxonList = [
	TaxonRef,
	TSComment,
	TSConst,
	TSModule,
	TSNamed,
	TSScalar,
	TSTypedef,
	TSTypeExprName,
	TSVar,
]

TSTaxonMap = {taxon.type : taxon for taxon in TSTaxonList}