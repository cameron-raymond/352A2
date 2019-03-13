import numpy as np
import os
from heapq import *


class Point:
    """
        Defines a point in the maze.
        Stores the location, cost and where they came from.
        Has methods to find neighbours.
    """
    def __init__(self, x, y, grid, came_from=None, cost_so_far=float('inf')):
        self.x = x
        self.y = y
        self.grid = grid
        self.came_from = came_from
        self.cost_so_far = cost_so_far

    def getXYNeighbours(self):
        """
            Finds the horizontal and vertical neighbours of the point.
        """
        neighbours = []
        x = self.x
        y = self.y
        grid = self.grid
        if x > 0 and grid[y][x-1] != 'X':
            neighbours.append(Point(x-1, y, grid, came_from=self))
        if x < len(grid[0])-1 and grid[y][x+1] != 'X':
            neighbours.append(Point(x+1, y, grid, came_from=self))
        if y > 0 and grid[y-1][x] != 'X':
            neighbours.append(Point(x, y-1, grid, came_from=self))
        if y < len(grid)-1 and grid[y+1][x] != 'X':
            neighbours.append(Point(x, y+1, grid, came_from=self))
        return neighbours

    def getDiagNeighbours(self):
        """
            Finds the diagonal neighbours of the point.
        """
        neighbours = []
        x = self.x
        y = self.y
        grid = self.grid
        if x>0 and y>0 and grid[y-1][x-1] != 'X': # up-left
            neighbours.append(Point(x-1, y-1, grid, came_from=self))
        if x>0 and y<len(grid)-1 and grid[y+1][x-1] != 'X': # down-left
            neighbours.append(Point(x-1, y+1, grid, came_from=self))
        if x<len(grid[0])-1 and y>0 and grid[y-1][x+1] != 'X': # up-right
            neighbours.append(Point(x+1, y-1, grid, came_from=self))
        if x<len(grid[0])-1 and y<len(grid)-1 and grid[y+1][x+1] != 'X': #down-right
            neighbours.append(Point(x+1, y+1, grid, came_from=self))
        return neighbours

    def __lt__(self, other):
        """
            Used to break ties in the priority queue.
            It doesn't matter which point comes earlier, so just return True.
        """
        return True


def readFile(filename):
    """
        Reads the grids from a text file.
        Saves them as 2D arrays
    """
    boards = []
    with open(filename) as f:
        file = f.readlines()
    board = []
    for row in file:
        if row == '\n':
            boards.append(board)
            board = []
        else:
            board.append(list(row.rstrip('\n')))
    boards.append(board)
    return boards

def writeOutput(grids):
    """
        Writes the solution to a text file.
    """
    with open("pathfinding_a_out.txt",'w') as out:
        for grid in grids:
            for row in grid:
                line = ''.join(row)+"\n"
                out.write(line)
            out.write("\n")

def AStar(grid, diagonal=False):
    """
        Solves the maze using the A* algorithm.
        The diagonal tag is True if we are allowed to move diagonal.
    """
    frontier = []
    start = findPoint('S', grid)
    start.cost_so_far = 0
    goal = findPoint('G', grid)
    heappush(frontier, (0, start))
    while not len(frontier)==0:
        current = heappop(frontier)[1]
        x = current.x
        y = current.y
        if grid[y][x] == '_':
            grid[y][x] = 'P'
        if grid[y][x] == 'G':
            break
        neighbours = current.getXYNeighbours(grid) \
            + (current.getDiagNeighbours(grid) if diagonal else [])
        for next in neighbours: #
            new_cost = current.cost_so_far + 1
            if new_cost < next.cost_so_far:
                next.cost_so_far = new_cost
                priority = new_cost + manhattan(goal, next)
                heappush(frontier, (priority, next))
                next.came_from = current
    return grid

def findPoint(target, grid):
    """
        Used to find the location of the start of goal.
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == target:
                return Point(col, row, grid)

def chebyshev(a, b):
    """
        The Chebyshev distance from a to b.
    """
    return max(abs(b.x-a.x), abs(b.y-a.y))

def manhattan(a, b):
    """
        The Manhattan distance from a to b.
    """
    return abs(b.x-a.x) + abs(b.y-a.y)

grids = readFile('pathfinding_a.txt')
solutions = []
for grid in grids:
    solutions.append(AStar(grid, diagonal=True))

writeOutput(solutions)
