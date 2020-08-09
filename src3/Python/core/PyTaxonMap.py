from core.TaxonComment import TaxonComment
from core.TaxonRef import TaxonRef
from core.TaxonScalar import TaxonScalar
from core.types.TaxonTypeExprName import TaxonTypeExprName
from Python.body.PyBody import PyBody
from Python.body.PyIf import PyIf
from Python.body.PyReturn import PyReturn
from Python.PyClass import PyClass
from Python.PyExpression import PyConst, PyNamed, PyCall
from Python.PyFunc import PyFunc, PyMethod
from Python.PyModule import PyModule
from Python.PyVar import PyParam, PyVar, PyField

PyTaxonList = [
	PyBody,
	PyCall,
	PyClass,
	PyConst,
	PyField,
	PyFunc,
	PyIf,
	PyMethod,
	PyModule,
	PyNamed,
	PyParam,
	PyReturn,
	PyVar,
	TaxonComment,
	TaxonRef,
	TaxonScalar,
	TaxonTypeExprName,
]

PyTaxonMap = {taxon.type : taxon for taxon in PyTaxonList}