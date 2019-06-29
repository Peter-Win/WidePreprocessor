from core.TaxonArray import TaxonArray
from Wpp.Context import Context
from Wpp.readWpp import readWpp
from Wpp.WppClass import WppClass
from Taxon import Taxon
from core.QuasiType import QuasiType

class WppArray(TaxonArray, WppClass):
	def init(self):
		content = """
field length: unsigned long
method push
	param item: Array.TItem
method pop: Array.TItem
		"""
		titem = self.addNamedItem(ArrayItemType(name='TItem'))
		titem.attrs.add('public')
		ctx = Context.createFromMemory(content)
		readWpp(ctx, self)

class ArrayItemType(Taxon):
	""" Тип элемента массива. Для проверки. Нужет только для WPP """
	type = 'ArrayItemType'
	def isType(self):
		return True
	def buildQuasiType(self):
		return QuasiType(self)
	def getDebugStr(self):
		return 'TItem'
	def exportString(self):
		return 'Array.TItem'
	def isReady(self):
		return True
	def isReadyFull(self):
		return True

	def findRealItemType(self, call):
		caller = call.getCaller()
		assert(caller.type == 'BinOp' and caller.opCode == '.')
		arrayInst = caller.getLeft() # variable or expression of array
		qtAI = arrayInst.buildQuasiType()
		assert(qtAI.taxon.type == 'Array')
		itemType = qtAI.itemType
		return itemType.buildQuasiType() # Это и есть тип элемента массива. К нему доджен подходить тип выражения справа

	def matchQuasiType(self, left, right):
		# right - using: list.push(22.2)
		# left - declaration: Array.push(value:ArrayItemType)
		# left: QuasiType 
		# +-taxon --> ArrayItemType
		# +-inst: TaxonCaller
		#   +-getCaller(): BinOp .
		#     +-getLeft(): TaxonIdExpr
		qtItem = self.findRealItemType(left.inst)
		return QuasiType.matchTaxons(qtItem, right)
	def matchQuasiTypeReverse(self, left, right):
		# Предполагается, что это конструкция типа x = list.pop()
		assert(right.taxon.type == 'ArrayItemType')
		if right.inst.type != 'Call':
			self.throwError('Expected type "Call" in right part (%s) instead of "%s"' % (right.inst.getDebugStr(), right.inst.type));
		qtItem = self.findRealItemType(right.inst) # examp: var x: double = listOfFloat.pop()   --> quasi of Scalar float
		return QuasiType.matchTaxons(left, qtItem)
