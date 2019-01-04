from Python.PyBlock import PyBlock
from Python.PyClass import PyClass
from Python.PyExpression import PyBinOp, PyCall, PyConst, PyFieldExpr, PyIdExpr, PyNull, PySuper, PyThis, PyTernaryOp
from Python.PyFunc import PyConstructor, PyFunc, PyMethod, PyOverloads
from Python.PyModule import PyModule
from Python.PyPackage import PyPackage
from Python.PyReturn import PyReturn
from Python.PyType import PyTypeName
from Python.PyVar import PyField, PyParam, PyVar

PyTaxonMap = {
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
	'Null': PyNull,
	'Overloads': PyOverloads,
	'Package': PyPackage,
	'Param': PyParam,
	'Return': PyReturn,
	'Super': PySuper,
	'This': PyThis,
	'TernaryOp': PyTernaryOp,
	'TypeName': PyTypeName,
	'Var': PyVar,
}