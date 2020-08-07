class TreeCtx:
	def __init__(self, level):
		self.level = level

def drawTaxonTree(taxon, ctx=None):
	s = ''
	level = 0
	if ctx:
		level = ctx.level
		s = level * '  '
	s += taxon.getDebugStr()
	print(s)
	for item in taxon.items:
		drawTaxonTree(item, TreeCtx(level+1))