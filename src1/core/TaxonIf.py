from Taxon import Taxon

class TaxonIf(Taxon):
	type = 'If'
	def getCases(self):
		""" Возвращает список пар (условие, блок). Минимум - один элемент в списке """
		cases = []
		i = 0
		n = len(self.items)
		while i < n - 1:
			cases.append((self.items[i], self.items[i+1]))
			i += 2
		return cases
		
	def getElse(self):
		""" Возвращает None или блок, если есть else """
		if len(self.items) % 2 == 0:
			return None
		return self.items[-1]
