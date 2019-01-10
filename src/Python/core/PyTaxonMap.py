from Python.PyBlock import PyBlock
from Python.PyClass import PyClass
from Python.PyExpression import PyArrayValue, PyBinOp, PyCall, PyConst, PyFieldExpr, PyIdExpr, PyNew, PyNull, PySuper, PyThis, PyTernaryOp, PyUnOp
from Python.PyFunc import PyConstructor, PyFunc, PyMethod, PyOverloads
from Python.PyModule import PyModule
from Python.PyPackage import PyPackage
from Python.PyReturn import PyReturn
from Python.PyType import PyTypeArray, PyTypeName
from Python.PyVar import PyField, PyParam, PyReadonly, PyVar

PyTaxonMap = {
	'ArrayValue': PyArrayValue,
	'BinOp': PyBinOp,
	'Block': PyBlock,
	'Call': PyCall,
	'Class': PyClass,
	'Const': PyConst,
	'Constructor': PyConstructor,
	'Field': PyField,
	'FieldExpr': PyFieldExpr,
	'Func': PyFunc,
	'IdExpr': PyIdExpr,
	'Method': PyMethod,
	'Module': PyModule,
	'New': PyNew,
	'Null': PyNull,
	'Overloads': PyOverloads,
	'Package': PyPackage,
	'Param': PyParam,
	'Readonly': PyReadonly,
	'Return': PyReturn,
	'Super': PySuper,
	'This': PyThis,
	'TernaryOp': PyTernaryOp,
	'TypeArray': PyTypeArray,
	'TypeName': PyTypeName,
	'UnOp': PyUnOp,
	'Var': PyVar,
}