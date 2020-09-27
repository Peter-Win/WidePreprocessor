from core.TaxonAltName import TaxonAltName
from core.TaxonComment import TaxonComment
from core.TaxonExtends import TaxonExtends
from core.TaxonOpDecl import TaxonDeclAssignBase
from core.TaxonRef import TaxonRef
from core.TaxonScalar import TaxonScalar
from core.types.TaxonTypeExprName import TaxonTypeExprName
from Python.body.PyBody import PyBody
from Python.body.PyIf import PyIf
from Python.body.PyReturn import PyReturn
from Python.PyClass import PyClass
from Python.PyExpression import PyBinOp, PyConst, PyNamed, PyCall, PyNew, PyMemberAccess, PyThis, PySuper
from Python.PyFunc import PyConstructor, PyFunc, PyMethod
from Python.PyModule import PyModule
from Python.PyOpDecl import PyDeclBinOp
from Python.PyOverload import PyOverload
from Python.PyVar import PyAutoinit, PyParam, PyVar, PyField

PyTaxonList = [
	PyAutoinit,
	PyBinOp,
	PyBody,
	PyCall,
	PyClass,
	PyConst,
	PyConstructor,
	PyDeclBinOp,
	PyField,
	PyFunc,
	PyIf,
	PyMemberAccess,
	PyMethod,
	PyModule,
	PyNamed,
	PyNew,
	PyOverload,
	PyParam,
	PyReturn,
	PySuper,
	PyThis,
	PyVar,
	TaxonAltName,
	TaxonComment,
	TaxonDeclAssignBase,
	TaxonExtends,
	TaxonRef,
	TaxonScalar,
	TaxonTypeExprName,
]

PyTaxonMap = {taxon.type : taxon for taxon in PyTaxonList}