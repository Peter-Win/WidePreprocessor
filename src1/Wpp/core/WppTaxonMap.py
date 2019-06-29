from Wpp.expr.Taxons import WppBinOp, WppConst, WppFieldExpr, WppIdExpr, WppVoid
from Wpp.WppBlock import WppBlock
from Wpp.WppFunc import WppOperator, WppOverloads
from Wpp.WppLocalType import WppTypeName
from Wpp.WppVar import WppParam, WppVar

WppTaxonMap = {
	'BinOp': WppBinOp,
	'Block': WppBlock,
	'Const': WppConst,
	'FieldExpr': WppFieldExpr,
	'IdExpr': WppIdExpr,
	'Operator': WppOperator,
	'Overloads': WppOverloads,
	'Param': WppParam,
	'TypeName': WppTypeName,
	'Var': WppVar,
	'Void': WppVoid,
}