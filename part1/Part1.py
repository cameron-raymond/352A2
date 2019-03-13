import numpy as np
import os
from heapq import *

class Point:
    def __init__(self, x, y, grid, came_from=None, cost_so_far=float('inf')):
        self.x = x
        self.y = y
        self.came_from = came_from
        self.cost_so_far = cost_so_far

    def getXYNeighbours(self, grid):
        neighbours = []
        x = self.x
        y = self.y
        if x > 0 and grid[y][x-1] != 'X':
            neighbours.append(Point(x-1, y, grid, came_from=self))
        if x < len(grid[0])-1 and grid[y][x+1] != 'X':
            neighbours.append(Point(x+1, y, grid, came_from=self))
        if y > 0 and grid[y-1][x] != 'X':
            neighbours.append(Point(x, y-1, grid, came_from=self))
        if y < len(grid)-1 and grid[y+1][x] != 'X':
            neighbours.append(Point(x, y+1, grid, came_from=self))
        return neighbours

    def getDiagNeighbours(self, grid):
        neighbours = []
        x = self.x
        y = self.y
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
        return True


def readFile(filename):
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
    with open("pathfinding_a_out.txt",'w') as out:
        for grid in grids:
            for row in grid:
                line = ''.join(row)+"\n"
                out.write(line)
            out.write("\n")

def AStar(grid, diagonal=False):
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
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == target:
                return Point(col, row, grid)

def chebyshev(a, b):
    return max(abs(b.x-a.x), abs(b.y-a.y))

def manhattan(a, b):
    return abs(b.x-a.x) + abs(b.y-a.y)

grids = readFile('pathfinding_a.txt')
solutions = []
for grid in grids:
    solutions.append(AStar(grid, diagonal=True))

writeOutput(solutions)
