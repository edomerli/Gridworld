from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
from collections import deque

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = deque()     # ONLY DIFFERENCE FROM DFS (apart from popleft() later)
            self.frontier.append(self.grid.start)
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0, self.grid.start)]
            self.explored = []
        elif self.type == "astar":
            self.frontier = [(self.H(self.grid.start), self.grid.start)]
            self.explored = []

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    # DFS
    def dfs_step(self):
        if len(self.frontier) == 0:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = self.frontier.pop()

        # Mark current node as explored
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]

        for n in children:
            # Check that it's inside the grid...
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                # ...and not a puddle
                if not self.grid.nodes[n].puddle:

                    # Ignore if it's already explored or currently in the frontier
                    if n not in self.explored and n not in self.frontier:

                        # Bookkeeping
                        self.previous[n] = current

                        # Check AT PUSH TIME if it's the goal, and if so terminate
                        if n == self.grid.goal:
                            self.finished = True
                            return

                        # Else add to frontier
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

    # BFS
    def bfs_step(self):
        if len(self.frontier) == 0:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = self.frontier.popleft()   # ONLY OTHER DIFFERENCE FROM DFS

        # Mark current node as explored
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]

        for n in children:
            # Check that it's inside the grid...
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                # ...and not a puddle
                if not self.grid.nodes[n].puddle:

                    # Ignore if it's already explored or currently in the frontier
                    if n not in self.explored and n not in self.frontier:

                        # Bookkeeping
                        self.previous[n] = current

                        # Check AT PUSH TIME if it's the goal, and if so terminate
                        if n == self.grid.goal:
                            self.finished = True
                            return

                        # Else add to frontier
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

    # UCS (a.k.a. Dijkstra)
    def ucs_step(self):
        if len(self.frontier) == 0:
            self.failed = True
            self.finished = True
            print("no path")
            return

        # Pop from frontier as a priority queue
        G_current, current = heappop(self.frontier)    # G(n) = "Real distance function of n from start"

        # Check AT POP TIME if it's the goal
        if current == self.grid.goal:
            self.finished = True
            return
        
        # Mark current node as explored
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False        

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]

        for n in children:
            # Check that it's inside the grid...
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                # ...and not a puddle
                if not self.grid.nodes[n].puddle:
                    G_n = G_current + (10 if self.grid.nodes[n].grass else 1)

                    # Ignore if it has been already explored
                    if n in self.explored:
                        continue

                    # If already in the frontier, check if needs to be updated
                    in_frontier = False
                    for i, (G, node) in enumerate(self.frontier):
                        if n == node:
                            in_frontier = True      # Mark as found

                            # Update if it has lower cost
                            if G_n < G:
                                self.previous[n] = current
                                self.frontier[i] = (G_n, n)
                            break

                    # Last case: unexplored
                    if not in_frontier:
                        # Bookkeeping
                        self.previous[n] = current

                        # Push to frontier
                        heappush(self.frontier, (G_n, n))
                        self.grid.nodes[n].color_frontier = True


    # A* (A star)
    def astar_step(self):
        if len(self.frontier) == 0:
            self.failed = True
            self.finished = True
            print("no path")
            return

        # Pop from frontier as a priority queue
        F_current, current = heappop(self.frontier)    # F(n) = G(n) + H(n)
        G_current = F_current - self.H(current)


        # Check AT POP TIME if it's the goal
        if current == self.grid.goal:
            self.finished = True
            return
        
        # Mark current node as explored
        self.explored.append(current)
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False        

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]

        for n in children:
            # Check that it's inside the grid...
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                # ...and not a puddle
                if not self.grid.nodes[n].puddle:
                    F_n = G_current + (10 if self.grid.nodes[n].grass else 1) + self.H(n)

                    # Ignore if it has been already explored
                    if n in self.explored:
                        continue

                    # If already in the frontier, check if needs to be updated
                    in_frontier = False
                    for i, (F, node) in enumerate(self.frontier):
                        if n == node:
                            in_frontier = True      # Mark as found

                            # Update if it has lower cost
                            if F_n < F:
                                self.previous[n] = current
                                self.frontier[i] = (F_n, n)

                                # re-establish the heap property!
                                heapify(self.frontier)
                            break

                    # Last case: unexplored
                    if not in_frontier:
                        # Bookkeeping
                        self.previous[n] = current

                        # Push to frontier
                        heappush(self.frontier, (F_n, n))
                        self.grid.nodes[n].color_frontier = True

    # Heuristic function for A*
    def H(self, n):
        # Defined as Manhattan distance to goal, downweighted to not be considered 
        # equal to actual distance G(.) in some edge cases
        return manhattan_dist(n, self.grid.goal)

# Manhattan distance
def manhattan_dist(n1, n2):
    return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])