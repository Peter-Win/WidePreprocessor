from core.TaxonClass import TaxonClass
from Python.PyTaxon import PyTaxon

class PyClass(TaxonClass, PyTaxon):
	def __init__(self):
		super().__init__()
		self.slots = None

	def onUpdate(self):
		if self.slots == None:
			self.slots = [i for i in self.items if i.type == 'Field' and 'static' not in i.attrs]
			if self.slots:
				self.updateConstructor()

	def updateConstructor(self):
		con = self.findConstructor()
		if not con:
			# Создать конструктор для инициализации переменных
			con = self.createEmptyConstructor()
			block = con.getBody()
			taxonMap = self.core.taxonMap
			for slot in self.slots:
				# block.addItem(eq)
				f = taxonMap['FieldExpr']()
				f.id = slot.getName(self)
				pt = taxonMap['BinOp']()
				pt.opCode = '.'
				pt.addItem(taxonMap['This']())
				pt.addItem(f)
				eq = taxonMap['BinOp']()
				eq.opCode = '='
				eq.addItem(pt)
				val0 = slot.getValueTaxon()
				val = val0.clone(self.core) if val0 else slot.getLocalType().getDefaultValue()
				eq.addItem(val)
				block.addItem(eq)

	def getDefaultValue(self):
		return self.core.taxonMap['Null']()

	def export(self, outContext):
		s = 'class ' + self.getName(self)
		parent = self.getParent()
		if parent:
			s += '(' + parent.getName(self) + ')'
		s += ':'
		outContext.writeln(s)
		outContext.level += 1
		# Comment
		self.exportComment(outContext)
		members = self.getMembers()
		if len(members) == 0:
			# No members in class. Not good, but possible
			outContext.writeln('pass')
		else:
			if self.slots:
				outContext.writeln('__slots__ = (' + ', '.join(["'"+i.getName(self)+"'" for i in self.slots]) + ')')
			for i in self.items:
				i.export(outContext)

		outContext.level -= 1