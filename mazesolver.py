#!/usr/bin/env python3

import sys
from math import floor
from math import sqrt
from PIL import Image
from queue import Queue
from priorityqueue import PriorityQueue

def convertMaze(maze):
    """
    px = maze.load()
    (width, height) = maze.size
    cellWidth = 0
    for x in range(width):
        if px[x,0] == (255,255,255,255):
            cellWidth += 1
    print(cellWidth)
    wallWidth = 2
    temp = width
    numCellWidth = 0
    while temp > 0:
        temp -= wallWidth
        if temp > cellWidth:
            temp -= cellWidth
            numCellWidth += 1
        elif temp != 0:
            raise TypeError("cannot determine number of cells in width of the maze")
    numCellHeight = 0
    if width == height:
        numCellHeight += numCellWidth
    else:
        temp = height
        while temp > 0:
            temp -= wallWidth
            if temp > cellWidth:
                temp -= cellWidth
                numCellHeight += 1
            elif temp != 0:
                raise TypeError("cannot determine number of cells in height of maze")

    print(numCellWidth)
    print(numCellHeight)

    mazeRepresentation = []
    adjacencyList = dict()
    
    x = wallWidth
    y = 0
    row = 0
    mazeRepresentation.append([])
    while x < width:
        if px[x,0] == (255,255,255,255):
            mazeRepresentation[0].append("S")
        else:
            mazeRepresentation[0].append("X")
        x += cellWidth
        x += wallWidth

    print(mazeRepresentation)
    """
    px = maze.load()
    (width, height) = maze.size
    mazeRepresentation = []
    for y in range(height):
        mazeRepresentation.append([])
        for x in range(width):
            if px[x,y] == (255,255,255,255):
                mazeRepresentation[y].append("O")
            elif px[x,y] == (0,0,0,255):
                mazeRepresentation[y].append("X")
            else:
                raise TypeError("invalid pixel found in maze. {0} found at {1}".format(px[x,y], (x,y)))

    start = ""
    while True:
        start = input("Start (x y):")
        start = start.split(" ")
        if len(start) == 2:
            for coord in range(len(start)):
                if start[coord].isnumeric():
                    start[coord] = int(start[coord])
                    if coord == 0:
                        if start[coord] not in range(width):
                            print("invalid x coordinate: out of range. x expected in range [0, {0}) got {1}".format(width, start[coord]))
                            start = None
                            break
                    else:
                        if start[coord] not in range(height):
                            print("invalid y coordinate: out of range. y expected in range [0, {0}) got {1}".format(height, start[coord]))
                            start = None
                            break
                else:
                    print("invalid coordinate. expected type int got {0}".format(type(start[coord])))
                    start = None
                    break
                        
        else:
            print("invalid number of coordinates. expected 2 got {0}".format(len(start)))
            print("x and y coordinates should be separated by a space")
            start = None
        
        if start is not None:
            (column, row) = start
            mazeRepresentation[row][column] = "S"
            break
    end = ""
    while True:
        end = input("end (x y):")
        end = end.split(" ")
        if len(end) == 2:
            for coord in range(len(end)):
                if end[coord].isnumeric():
                    end[coord] = int(end[coord])
                    if coord == 0:
                        if end[coord] not in range(width):
                            print("invalid x coordinate: out of range. x expected in range [0, {0}) got {1}".format(width, end[coord]))
                            end = None
                            break
                    else:
                        if end[coord] not in range(height):
                            print("invalid y coordinate: out of range. y expected in range [0, {0}) got {1}".format(height, end[coord]))
                            end = None
                            break
                else:
                    print("invalid coordinate. expected type int got {0}".format(type(end[coord])))
                    end = None 
                    break
        else:
            print("invalid number of coordinates. expected 2 got {0}".format(len(end)))
            print("x and y coordinates should be separated by a space")
            end = None
            
        if end is not None:
            (column, row) = end
            mazeRepresentation[row][column] = "E"
            break
        
    return (mazeRepresentation, start, end)

def chebyshevDistance(c1, c2):
    if not isinstance(c1, list):
        return -1
    if not isinstance(c2, list):
        return -1
    (c1R, c1C) = c1
    (c2R, c2C) = c2
    x_dist = abs(c1R - c2R)
    y_dist = abs(c1C - c2C)
    return max(y_dist, x_dist)

def manhattanDistance(c1, c2):
    (c1R, c1C) = c1
    (c2R, c2C) = c2
    return abs(c1R - c2R) + abs(c1C - c2C)

def bfs(maze, start, diagonals):
    start = [start[1], start[0]]

    paths = dict()
    visited = set()
    queue = Queue()
    queue.enQueue(start)
    paths[repr(start)] = "Start"
    while not queue.isEmpty():
        current = queue.deQueue()
        if repr(current) not in visited:
            (x, y) = current
            if maze[x][y] == "E":
                return (paths, current)

            def isValid(cell, maze):
                if not isinstance(cell, list):
                    return False
                return cell[0] in range(len(maze)) and cell[1] in range(len(maze[cell[0]]))

            W = [x, y - 1]
            if isValid(W, maze) and repr(W) not in visited:
                if maze[W[0]][W[1]] != "X":
                    queue.enQueue(W)
                    if repr(W) not in paths:
                        paths[repr(W)] = current

            E = [x, y + 1]
            if isValid(E, maze) and repr(E) not in visited:
                if maze[E[0]][E[1]] != "X":
                    queue.enQueue(E)
                    if repr(E) not in paths:
                        paths[repr(E)] = current

            N = [x - 1, y]
            if isValid(N, maze) and repr(N) not in visited:
                if maze[N[0]][N[1]] != "X":
                    queue.enQueue(N)
                    if repr(N) not in paths:
                        paths[repr(N)] = current

            S = [x + 1, y]
            if isValid(S, maze) and repr(S) not in visited:
                if maze[S[0]][S[1]] != "X":
                    queue.enQueue(S)
                    if repr(S) not in paths:
                        paths[repr(S)] = current
            
            if diagonals:
                NW = [x - 1, y - 1]
                if isValid(NW, maze) and repr(NW) not in visited:
                    if maze[NW[0]][NW[1]] != "X":
                        queue.enQueue(NW)
                        if repr(NW) not in paths:
                            paths[repr(NW)] = current

                SW = [x + 1, y - 1]
                if isValid(SW, maze) and repr(SW) not in visited:
                    if maze[SW[0]][SW[1]] != "X":
                        queue.enQueue(SW)
                        if repr(SW) not in paths:
                            paths[repr(SW)] = current
            
                NE = [x - 1, y + 1]
                if isValid(NE, maze) and repr(NE) not in visited:
                    if maze[NE[0]][NE[1]] != "X":
                        queue.enQueue(NE)
                        if repr(NE) not in paths:
                            paths[repr(NE)] = current

                SE = [x + 1, y + 1]
                if isValid(SE, maze) and repr(SE) not in visited:
                    if maze[SE[0]][SE[1]] != "X":
                        queue.enQueue(SE)
                        if repr(SE) not in paths:
                            paths[repr(SE)] = current

            visited.add(repr(current))

    return None

def dijkstrasAlgorithm(maze, start, diagonals):
    start = [start[1], start[0]]
    distance = dict()
    paths = dict()
    visited = set()
    distance[repr(start)] = 0
    paths[repr(start)] = "Start"
    pq = PriorityQueue()
    pq.enQueue(distance[repr(start)],start)

    while not pq.isEmpty():
        current = pq.deQueue()
        if repr(current) not in visited:
            (x, y) = current
            if maze[x][y] == "E":
                return (paths, current)
            #print("{0}: {1}".format(current, distance[repr(current)]))
            def isValid(cell, maze):
                if not isinstance(cell, list):
                    return False
                return cell[0] in range(len(maze)) and cell[1] in range(len(maze[cell[0]]))
            
            W = [x, y - 1]
            if isValid(W, maze):
                (row, column) = W
                if maze[row][column] != "X":
                    if repr(W) not in distance:
                        distance[repr(W)] = distance[repr(current)] + 1
                        paths[repr(W)] = current
                        pq.enQueue(distance[repr(W)], W)
                    else:
                        if distance[repr(W)] >  distance[repr(current)] + 1:
                            distance[repr(W)] = distance[repr(current)] + 1
                            paths[repr(W)] = current
                            pq.update(W, distance[repr(W)])
            
            E = [x, y + 1]
            if isValid(E, maze):
                (row, column) = E
                if maze[row][column] != "X":
                    if repr(E) not in distance:
                        distance[repr(E)] = distance[repr(current)] + 1
                        paths[repr(E)] = current
                        pq.enQueue(distance[repr(E)], E)
                    else:
                        if distance[repr(E)] >  distance[repr(current)] + 1:
                            distance[repr(E)] = distance[repr(current)] + 1
                            paths[repr(E)] = current
                            pq.update(E, distance[repr(E)])

            N = [x - 1, y] 
            
            if isValid(N, maze):
                (row, column) = N
                if maze[row][column] != "X":
                    if repr(N) not in distance:
                        distance[repr(N)] = distance[repr(current)] + 1
                        paths[repr(N)] = current
                        pq.enQueue(distance[repr(N)], N)
                    else:
                        if distance[repr(N)] >  distance[repr(current)] + 1:
                            distance[repr(N)] = distance[repr(current)] + 1
                            paths[repr(N)] = current
                            pq.update(N, distance[repr(N)])

            S = [x + 1, y]

            if isValid(S, maze):
                (row, column) = S
                if maze[row][column] != "X":
                    if repr(S) not in distance:
                        distance[repr(S)] = distance[repr(current)] + 1
                        paths[repr(S)] = current
                        pq.enQueue(distance[repr(S)], S)
                    else:
                        if distance[repr(S)] >  distance[repr(current)] + 1:
                            distance[repr(S)] = distance[repr(current)] + 1
                            paths[repr(S)] = current
                            pq.update(S, distance[repr(S)])
            

            if diagonals:
                
                NW = [x - 1, y - 1]
                if isValid(NW, maze):
                    (row, column) = NW
                    if maze[row][column] != "X":
                        if repr(NW) not in distance:
                            distance[repr(NW)] = distance[repr(current)] + 1
                            paths[repr(NW)] = current
                            pq.enQueue(distance[repr(NW)], NW)
                        else:
                            if distance[repr(NW)] >  distance[repr(current)] + 1:
                                distance[repr(NW)] = distance[repr(current)] + 1
                                paths[repr(NW)] = current
                                pq.update(NW, distance[repr(NW)])
            
                NE = [x - 1, y + 1]
                if isValid(NE, maze):
                    (row, column) = NE
                    if maze[row][column] != "X":
                        if repr(NE) not in distance:
                            distance[repr(NE)] = distance[repr(current)] + 1
                            paths[repr(NE)] = current
                            pq.enQueue(distance[repr(NE)], NE)
                        else:
                            if distance[repr(NE)] >  distance[repr(current)] + 1:
                                distance[repr(NE)] = distance[repr(current)] + 1
                                paths[repr(NE)] = current
                                pq.update(NE, distance[repr(NE)])

                SW = [x + 1, y - 1]
                if isValid(SW, maze):
                    (row, column) = SW
                    if maze[row][column] != "X":
                        if repr(SW) not in distance:
                            distance[repr(SW)] = distance[repr(current)] + 1
                            paths[repr(SW)] = current
                            pq.enQueue(distance[repr(SW)], SW)
                        else:
                            if distance[repr(SW)] >  distance[repr(current)] + 1:
                                distance[repr(SW)] = distance[repr(current)] + 1
                                paths[repr(SW)] = current
                                pq.update(SW, distance[repr(SW)])
            
                SE = [x + 1, y + 1]
                if isValid(SE, maze):
                    (row, column) = SE
                    if maze[row][column] != "X":
                        if repr(SE) not in distance:
                            distance[repr(SE)] = distance[repr(current)] + 1
                            paths[repr(SE)] = current
                            pq.enQueue(distance[repr(SE)], SE)
                        else:
                            if distance[repr(SE)] >  distance[repr(current)] + 1:
                                distance[repr(SE)] = distance[repr(current)] + 1
                                paths[repr(SE)] = current
                                pq.update(SE, distance[repr(SE)])

            visited.add(repr(current))
    return None


def AStarSearch(maze, start, end, diagonals):
    start = [start[1], start[0]]
    end = [end[1], end[0]]
    distance = dict()
    paths = dict()
    visited = set()

    def isValid(cell, maze):
        if not isinstance(cell, list):
            return False
        return cell[0] in range(len(maze)) and cell[1] in range(len(maze[cell[0]]))

    def g(cell, distance):
        return distance[repr(cell)]

    def h(cell, end, diagonals):
        if diagonals:
            return chebyshevDistance(cell, end)
        else:
            return manhattanDistance(cell, end)
    
    f = lambda e: (g(e, distance) + h(e, end, diagonals), h(e, end, diagonals))
    
    distance[repr(start)] = 0
    paths[repr(start)] = "Start"
    pq = PriorityQueue(priorityType = tuple)
    pq.enQueue(f(start), start)

    while not pq.isEmpty():
        current = pq.deQueue()
        if repr(current) not in visited:
            #print("{0}: {1}".format(current, f(current)))
            (x, y) = current
            if maze[x][y] == "E":
                return (paths, current)
            
            W = [x, y - 1]
            if isValid(W, maze):
                (row, column) = W
                if maze[row][column] != "X":
                    if repr(W) not in distance:
                        distance[repr(W)] = distance[repr(current)] + 1
                        paths[repr(W)] = current
                        pq.enQueue(f(W), W)
                    else:
                        if distance[repr(W)] >  distance[repr(current)] + 1:
                            distance[repr(W)] = distance[repr(current)] + 1
                            paths[repr(W)] = current
                            pq.update(W, f(W))


            E = [x, y + 1]
            if isValid(E, maze):
                (row, column) = E
                if maze[row][column] != "X":
                    if repr(E) not in distance:
                        distance[repr(E)] = distance[repr(current)] + 1
                        paths[repr(E)] = current
                        pq.enQueue(f(E), E)
                    else:
                        if distance[repr(E)] >  distance[repr(current)] + 1:
                            distance[repr(E)] = distance[repr(current)] + 1
                            paths[repr(E)] = current
                            pq.update(E, f(E))

            N = [x - 1, y] 
            if isValid(N, maze):
                (row, column) = N
                if maze[row][column] != "X":
                    if repr(N) not in distance:
                        distance[repr(N)] = distance[repr(current)] + 1
                        paths[repr(N)] = current
                        pq.enQueue(f(N), N)
                    else:
                        if distance[repr(N)] >  distance[repr(current)] + 1:
                            distance[repr(N)] = distance[repr(current)] + 1
                            paths[repr(N)] = current
                            pq.update(N, f(N))


            S = [x + 1, y] 
            if isValid(S, maze):
                (row, column) = S
                if maze[row][column] != "X":
                    if repr(S) not in distance:
                        distance[repr(S)] = distance[repr(current)] + 1
                        paths[repr(S)] = current
                        pq.enQueue(f(S), S)
                    else:
                        if distance[repr(S)] >  distance[repr(current)] + 1:
                            distance[repr(S)] = distance[repr(current)] + 1
                            paths[repr(S)] = current
                            pq.update(S, f(S))
            

            if diagonals:
                NW = [x - 1, y - 1]
                if isValid(NW, maze):
                    (row, column) = NW
                    if maze[row][column] != "X":
                        if repr(NW) not in distance:
                            distance[repr(NW)] = distance[repr(current)] + 1
                            paths[repr(NW)] = current
                            pq.enQueue(f(NW), NW)
                        else:
                            if distance[repr(NW)] >  distance[repr(current)] + 1:
                                distance[repr(NW)] = distance[repr(current)] + 1
                                paths[repr(NW)] = current
                                pq.update(NW, f(NW))

                SW = [x + 1, y - 1]
                if isValid(SW, maze):
                    (row, column) = SW
                    if maze[row][column] != "X":
                        if repr(SW) not in distance:
                            distance[repr(SW)] = distance[repr(current)] + 1
                            paths[repr(SW)] = current
                            pq.enQueue(f(SW), SW)
                        else:
                            if distance[repr(SW)] >  distance[repr(current)] + 1:
                                distance[repr(SW)] = distance[repr(current)] + 1
                                paths[repr(SW)] = current
                                pq.update(SW, f(SW))
            
                NE = [x - 1, y + 1]
                if isValid(NE, maze):
                    (row, column) = NE
                    if maze[row][column] != "X":
                        if repr(NE) not in distance:
                            distance[repr(NE)] = distance[repr(current)] + 1
                            paths[repr(NE)] = current
                            pq.enQueue(f(NE), NE)
                        else:
                            if distance[repr(NE)] >  distance[repr(current)] + 1:
                                distance[repr(NE)] = distance[repr(current)] + 1
                                paths[repr(NE)] = current
                                pq.update(NE, f(NE))

                SE = [x + 1, y + 1]
                if isValid(SE, maze):
                    (row, column) = SE
                    if maze[row][column] != "X":
                        if repr(SE) not in distance:
                            distance[repr(SE)] = distance[repr(current)] + 1
                            paths[repr(SE)] = current
                            pq.enQueue(f(SE), SE)
                        else:
                            if distance[repr(SE)] >  distance[repr(current)] + 1:
                                distance[repr(SE)] = distance[repr(current)] + 1
                                paths[repr(SE)] = current
                                pq.update(SE, f(SE))

            visited.add(repr(current))

    return None
def solve(mazeRep):
    (maze, start, end) = mazeRep
    result = None
    while True:
        print("1: Dijkstra's lgorithm")
        print("2: A* search Algorithm")
        print("3: Breadth First Search")
        print("4: Dijkstra's Algorithm(Diagonals Enabled)")
        print("5: A* Search Algorithm(Diagonals Enabled)")
        print("6: Breadth First Search(Diagonals Enabled)")
        uInput = input("Make a selection: ")
        if uInput == "1":
            result = dijkstrasAlgorithm(maze, start, False)
            break
        elif uInput == "2":
            result = AStarSearch(maze, start, end, False)
            break
        elif uInput == "3":
            result = bfs(maze, start, False)
            break
        elif uInput == "4":
            result = dijkstrasAlgorithm(maze, start, True)
            break
        elif uInput == "5":
            result = AStarSearch(maze, start, end, True)
            break
        elif uInput == "6":
            result = bfs(maze, start, True)
            break
        else:
            print("invalid selection {}".format(uInput))
    return result


if len(sys.argv) < 2:
    raise ValueError("maze image must be provided")

maze = None

try:
    maze = Image.open(sys.argv[1])
except FileNotFoundError:
    raise FileNotFoundError("{0} does not exist".format(sys.argv[1]))

mazeRep = convertMaze(maze)
result = solve(mazeRep)
if result is None:
    print("No Path Found")
    (junk, start, end) = mazeRep
    (startX, startY) = start
    (endX, endY) = end
    px = maze.load()
    px[startX, startY] = (0, 0, 255, 255)
    px[endX, endY] = (255, 0, 0, 255)
    maze.show()
    quit()
(paths, end) = result
path = []
while paths[repr(end)] != "Start":
    path.insert(0, end)
    end = paths[repr(end)]

path.insert(0, end)
print(len(path))

px = maze.load()

for cell in range(len(path)):
    (y, x) = path[cell]
    px[x,y] = (floor(cell / (len(path) - 1) * 255), 0, floor(((len(path) - 1) - cell) / (len(path) - 1) * 255), 255)

maze.show()
