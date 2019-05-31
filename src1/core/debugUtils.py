def recursiveDebugStr(taxon, level = 0):
	print('%s%s:%s => %s, ready=%s, readyFull=%s' % ('  '*level, taxon.type, taxon.name, taxon.getDebugStr(), taxon.isReady(), taxon.isReadyFull()))
	for item in taxon.items:
		recursiveDebugStr(item, level + 1)