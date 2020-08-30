from core.TaxonComment import TaxonComment
from core.TaxonOpDecl import TaxonDeclAssignBase
from core.TaxonRef import TaxonRef
from core.TaxonScalar import TaxonScalar
from core.types.TaxonTypeExprName import TaxonTypeExprName
from Python.body.PyBody import PyBody
from Python.body.PyIf import PyIf
from Python.body.PyReturn import PyReturn
from Python.PyClass import PyClass
from Python.PyExpression import PyBinOp, PyConst, PyNamed, PyCall, PyNew, PyMemberAccess
from Python.PyFunc import PyConstructor, PyFunc, PyMethod
from Python.PyModule import PyModule
from Python.PyVar import PyAutoinit, PyParam, PyVar, PyField

PyTaxonList = [
	PyAutoinit,
	PyBinOp,
	PyBody,
	PyCall,
	PyClass,
	PyConst,
	PyConstructor,
	PyField,
	PyFunc,
	PyIf,
	PyMemberAccess,
	PyMethod,
	PyModule,
	PyNamed,
	PyNew,
	PyParam,
	PyReturn,
	PyVar,
	TaxonComment,
	TaxonDeclAssignBase,
	TaxonRef,
	TaxonScalar,
	TaxonTypeExprName,
]

PyTaxonMap = {taxon.type : taxon for taxon in PyTaxonList}