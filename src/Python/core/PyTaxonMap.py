from Python.PyBlock import PyBlock
from Python.PyCast import PyCast
from Python.PyClass import PyClass
from Python.PyExpression import PyArrayValue, PyBinOp, PyCall, PyConst, PyFieldExpr, PyIdExpr, PyNew, PyNull, PySuper, PyThis, PyTernaryOp, PyUnOp, PyTrue, PyFalse
from Python.PyForeach import PyForeach
from Python.PyFunc import PyConstructor, PyFunc, PyMethod, PyOverloads
from Python.PyIf import PyIf
from Python.PyModule import PyModule
from Python.PyOperator import PyOperator
from Python.PyPackage import PyPackage
from Python.PyReturn import PyReturn
from Python.PyType import PyTypeArray, PyTypeMap, PyTypeName, PyTypePath
from Python.PyTypedef import PyTypedef
from Python.PyVar import PyField, PyParam, PyReadonly, PyVar

PyTaxonMap = {
	'ArrayValue': PyArrayValue,
	'BinOp': PyBinOp,
	'Block': PyBlock,
	'Call': PyCall,
	'Cast': PyCast,
	'Class': PyClass,
	'Const': PyConst,
	'Constructor': PyConstructor,
	'False': PyFalse,
	'Field': PyField,
	'FieldExpr': PyFieldExpr,
	'Foreach': PyForeach,
	'Func': PyFunc,
	'IdExpr': PyIdExpr,
	'If': PyIf,
	'Method': PyMethod,
	'Module': PyModule,
	'New': PyNew,
	'Null': PyNull,
	'Operator': PyOperator,
	'Overloads': PyOverloads,
	'Package': PyPackage,
	'Param': PyParam,
	'Readonly': PyReadonly,
	'Return': PyReturn,
	'Super': PySuper,
	'TernaryOp': PyTernaryOp,
	'This': PyThis,
	'True': PyTrue,
	'TypeArray': PyTypeArray,
	'Typedef': PyTypedef,
	'TypeMap': PyTypeMap,
	'TypeName': PyTypeName,
	'TypePath': PyTypePath,
	'UnOp': PyUnOp,
	'Var': PyVar,
}