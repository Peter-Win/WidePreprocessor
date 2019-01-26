from core.TaxonPackage import TaxonPackage
from TS.TsBlock import TsBlock
from TS.TsClass import TsClass
from TS.TsExpression import TsArrayValue, TsBinOp, TsCall, TsConst, TsFalse, TsFieldExpr, TsIdExpr, TsNew, TsNull, TsSuper, TsTernaryOp, TsThis, TsTrue, TsUnaryOp
from TS.TsFunc import TsConstructor, TsFunc, TsMethod, TsOverloads
from TS.TsModule import TsModule
from TS.TsReturn import TsReturn
from TS.TsType import TsTypeName, TsTypePath, TsTypeArray, TsTypeMap
from TS.TsVar import TsVar, TsField, TsReadonly, TsParam

TsTaxonMap = {
	'ArrayValue': TsArrayValue,
	'BinOp': TsBinOp,
	'Block': TsBlock,
	'Call': TsCall,
	'Const': TsConst,
	'Constructor': TsConstructor,
	'Class': TsClass,
	'False': TsFalse,
	'Field': TsField,
	'FieldExpr': TsFieldExpr,
	'Func': TsFunc,
	'IdExpr': TsIdExpr,
	'Method': TsMethod,
	'Module': TsModule,
	'New': TsNew,
	'Null': TsNull,
	'Overloads': TsOverloads,
	'Package': TaxonPackage,
	'Param': TsParam,
	'Readonly': TsReadonly,
	'Return': TsReturn,
	'Super': TsSuper,
	'TernaryOp': TsTernaryOp,
	'This': TsThis,
	'True': TsTrue,
	'TypeArray': TsTypeArray,
	'TypeMap': TsTypeMap,
	'TypeName': TsTypeName,
	'TypePath': TsTypePath,
	'UnOp': TsUnaryOp,
	'Var': TsVar,
}