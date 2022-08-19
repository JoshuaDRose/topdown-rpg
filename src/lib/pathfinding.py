from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder as Finder

def find_path(matrix, end, start=(0,0)):
	"""
		matrix: list matrix with integers
		start: start position
		end: end position
	"""
	start = grid.node(start)
	end = grid.node(end)

	finder = Finder()

	path, runs = finder.find_path(start, end)

	return path