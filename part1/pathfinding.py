import numpy as np
import os
from heapq import *

class Graph:
    """
        Defines a maze.
        Stores the maze as a 2d array.
        Had methods to solve the maze.
    """
    def __init__(self, grid):
        self.grid = grid
        self.start = self.findPoint('S')
        self.goal = self.findPoint('G')

    def findPoint(self, target):
        """
            Used to find the location of the start of goal.
        """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == target:
                    return Point(col, row)

    def greedy(self, diagonal=False):
        """
            Solves the maze using a greedy algorithm.
            The diagonal tag is True if we are allowed to move diagonal.
        """
        frontier = []
        visited = [[False for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        start = self.start
        goal = self.goal
        heappush(frontier, (0, start))
        while not len(frontier)==0:
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.grid[y][x] == 'G':
                break
            neighbours = self.getXYNeighbours(current) \
                + (self.getDiagNeighbours(current) if diagonal else [])
            for next in neighbours:
                if not visited[next.y][next.x]:
                    heuristic = self.chebyshev(goal, next) if diagonal else self.manhattan(goal, next)
                    priority = heuristic
                    heappush(frontier, (priority, next))
                    visited[y][x] = True
                    next.came_from = current
        solution = self.grid
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution

    def AStar(self, diagonal=False):
        """
            Solves the maze using the A* algorithm.
            The diagonal tag is True if we are allowed to move diagonal.
        """
        frontier = []
        start = self.start
        start.cost_so_far = 0
        goal = self.goal
        heappush(frontier, (0, start))
        while not len(frontier)==0:
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.grid[y][x] == 'G':
                break
            neighbours = self.getXYNeighbours(current) \
                + (self.getDiagNeighbours(current) if diagonal else [])
            for next in neighbours:
                new_cost = current.cost_so_far + 1
                if new_cost < next.cost_so_far:
                    next.cost_so_far = new_cost
                    heuristic = self.chebyshev(goal, next) if diagonal else self.manhattan(goal, next)
                    priority = new_cost + heuristic
                    heappush(frontier, (priority, next))
                    next.came_from = current
        solution = self.grid
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution

    def getXYNeighbours(self, p):
        """
            Finds the horizontal and vertical neighbours of the point.
        """
        neighbours = []
        x = p.x
        y = p.y
        grid = self.grid
        if x > 0 and grid[y][x-1] != 'X':
            neighbours.append(Point(x-1, y, came_from=p))
        if x < len(grid[0])-1 and grid[y][x+1] != 'X':
            neighbours.append(Point(x+1, y, came_from=p))
        if y > 0 and grid[y-1][x] != 'X':
            neighbours.append(Point(x, y-1, came_from=p))
        if y < len(grid)-1 and grid[y+1][x] != 'X':
            neighbours.append(Point(x, y+1, came_from=p))
        return neighbours

    def getDiagNeighbours(self, p):
        """
            Finds the diagonal neighbours of the point.
        """
        neighbours = []
        grid = self.grid
        x = p.x
        y = p.y
        if x>0 and y>0 and grid[y-1][x-1] != 'X': # up-left
            neighbours.append(Point(x-1, y-1, came_from=p))
        if x>0 and y<len(grid)-1 and grid[y+1][x-1] != 'X': # down-left
            neighbours.append(Point(x-1, y+1, came_from=p))
        if x<len(grid[0])-1 and y>0 and grid[y-1][x+1] != 'X': # up-right
            neighbours.append(Point(x+1, y-1, came_from=p))
        if x<len(grid[0])-1 and y<len(grid)-1 and grid[y+1][x+1] != 'X': #down-right
            neighbours.append(Point(x+1, y+1, came_from=p))
        return neighbours

    def chebyshev(self, a, b):
        """
            The Chebyshev distance from a to b.
        """
        return max(abs(b.x-a.x), abs(b.y-a.y))

    def manhattan(self, a, b):
        """
            The Manhattan distance from a to b.
        """
        return abs(b.x-a.x) + abs(b.y-a.y)

class Point:
    """
        Defines a point in the maze.
        Stores the location, cost and where they came from.
    """
    def __init__(self, x, y, came_from=None, cost_so_far=float('inf'), visited=False):
        self.x = x
        self.y = y
        self.came_from = came_from
        self.cost_so_far = cost_so_far
        self.visited = visited

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

def writeOutput(greedySolutions, AStarSolutions, filename):
    """
        Writes the solution to a text file.
    """
    with open(filename,'w') as out:
        for ind in range(len(greedySolutions)):
            out.write('Greedy\n')
            for row in greedySolutions[ind]:
                line = ''.join(row)+"\n"
                out.write(line)
            out.write('A*\n')
            for row in AStarSolutions[ind]:
                line = ''.join(row)+"\n"
                out.write(line)
            out.write("\n")

def solveXY():
    '''
        Solves the graphs, allowing only vertical and horizontal movement
    '''
    grids = readFile('pathfinding_a.txt')
    greedySolutions = []
    AStarSolutions = []
    for grid in grids:
        maze = Graph(grid)
        greedySolutions.append(maze.greedy(diagonal=False))
        AStarSolutions.append(maze.AStar(diagonal=False))
    writeOutput(greedySolutions, AStarSolutions, 'pathfinding_a_out.txt')

def solveDiag():
    '''
        Solves the graphs, allowing diagonal movement as well as vertical/horizontal
    '''
    grids = readFile('pathfinding_b.txt')
    greedySolutions = []
    AStarSolutions = []
    for grid in grids:
        maze = Graph(grid)
        greedySolutions.append(maze.greedy(diagonal=True))
        AStarSolutions.append(maze.AStar(diagonal=True))
    writeOutput(greedySolutions, AStarSolutions, 'pathfinding_b_out.txt')

solveXY()
solveDiag()
