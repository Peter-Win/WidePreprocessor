from core.TaxonRef import TaxonRef
from TS.core.TSScalar import TSScalar
from TS.TSExpression import TSConst
from TS.TSModule import TSModule
from TS.TSTypedef import TSTypedef
from TS.TSTypeExpr import TSTypeExprName
from TS.TSVar import TSVar

TSTaxonList = [
	TaxonRef,
	TSConst,
	TSModule,
	TSScalar,
	TSTypedef,
	TSTypeExprName,
	TSVar,
]

TSTaxonMap = {taxon.type : taxon for taxon in TSTaxonList}