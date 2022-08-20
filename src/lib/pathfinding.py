""" Ai pathfinder """
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder as Finder

def find_path(matrix, end, start=(0,0)):
    """
        matrix: list matrix with integers
        start: start position
        end: end position
    """
    start = matrix.node(start)
    end = matrix.node(end)
    finder = Finder()
    # path, runs = finder.find_path(start, end)
    # pylint: disable=E1120
    return finder.find_path(start, end)
