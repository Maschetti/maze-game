import numpy as np
import tkinter as tk
import time

WALL = '#'
EMPTY = ' '
PATH = '*'
PLAYER = 'p'
EXIT = 'E'

CELL_SIZE = 40

class Maze:
    def __init__(self, height, width, root, pobs=0.25, delay=0.3):
        self.delay = delay
        self.cell_size = CELL_SIZE if (height < 25) and (width < 50) else CELL_SIZE // 2

        self.maze = np.full((height, width), EMPTY, dtype=str)
        self.start = [0, 0]
        self.exit = [self.maze.shape[0] - 1, self.maze.shape[1] - 1]
        self.set_walls(pobs)

        # Set the player and exit in the maze
        self.maze[self.start[0]][self.start[1]] = PLAYER
        self.maze[self.exit[0]][self.exit[1]] = EXIT

        self.root = root
        self.root.title("Maze Solver")
        
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.dfs_button = tk.Button(self.buttons_frame, text="DFS", command=self.dfs)
        self.dfs_button.pack(fill=tk.X)
        
        self.bfs_button = tk.Button(self.buttons_frame, text="BFS", command=self.bfs)
        self.bfs_button.pack(fill=tk.X)
        
        self.astarh1_button = tk.Button(self.buttons_frame, text="A*h1", command=self.a_star_manhattan)
        self.astarh1_button.pack(fill=tk.X)
        
        self.astarh2_button = tk.Button(self.buttons_frame, text="A*h2", command=self.a_start_euclidean)
        self.astarh2_button.pack(fill=tk.X)

        self.canvas = tk.Canvas(root, width=width * self.cell_size, height=height * self.cell_size)
        self.canvas.pack()
        
        self.set_colors()

        self.is_running = False

    def reset_maze(self):
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i][j] == PATH or self.maze[i][j] == PLAYER:
                    self.maze[i][j] = EMPTY

        self.update_interface()

    def set_walls(self, pobs):
        obstacles = np.random.rand(*self.maze.shape) < pobs
        self.maze[obstacles] = WALL
    
    def get_neighbors(self, pos):
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        candidates = np.array([pos + dir for dir in directions])
        neighbors = [c for c in candidates if (c[0] >= 0 and c[0] < self.maze.shape[0]) and (c[1] >= 0 and c[1] < self.maze.shape[1]) and (self.maze[c[0]][c[1]] != WALL)]
        return neighbors

    def set_colors(self):
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                color = "white"
                if self.maze[i][j] == WALL:
                    color = "black"
                elif self.maze[i][j] == PLAYER:
                    color = "green"
                elif self.maze[i][j] == EXIT:
                    color = "red"
                elif self.maze[i][j] == PATH:
                    color = "yellow"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size, j * self.cell_size + self.cell_size, i * self.cell_size + self.cell_size, fill=color, outline="gray")

    def update_interface(self):
        self.canvas.delete('all')
        self.set_colors()
        self.root.update()
        time.sleep(self.delay)

    def dfs(self):
        self.is_running = True
        self.reset_maze()
        frontier = [[self.start]]
        visited = [self.start]

        while frontier and self.is_running:
            path = frontier.pop(-1)

            pos = path[-1]
            self.maze[pos[0]][pos[1]] = PLAYER
            self.update_interface()

            if np.array_equal(self.exit, pos):
                self.is_running = False
                return path, visited
            
            self.maze[pos[0]][pos[1]] = PATH
            
            neighbors = self.get_neighbors(pos)
            for n in neighbors:
                if not(any(np.array_equal(n, v) for v in visited)):
                    visited.append(n)
                    frontier.append(path + [n])
        self.is_running = False
        return None, None

    def bfs(self):
        self.is_running = False  # Stop any ongoing search
        self.is_running = True
        self.reset_maze()
        frontier = [[self.start]]
        visited = [self.start]

        while frontier and self.is_running:
            path = frontier.pop(0)

            pos = path[-1]
            self.maze[pos[0]][pos[1]] = PLAYER
            self.update_interface()

            if np.array_equal(self.exit, pos):
                self.is_running = False
                return path, visited
            
            self.maze[pos[0]][pos[1]] = PATH
            
            neighbors = self.get_neighbors(pos)
            for n in neighbors:
                if not(any(np.array_equal(n, v) for v in visited)):
                    visited.append(n)
                    frontier.append(path + [n])
        self.is_running = False
        return None, None
    
    def manhattan(self, pos):
        y = pos[0] - self.exit[0]
        x = pos[1] - self.exit[1]
        if y < 0:
            y = -1 * y
        if x < 0:
            x = -1 * x
        return x + y

    def euclidean(self, pos):
        return np.sqrt((pos[0] - self.exit[0])**2 + (pos[1] - self.exit[1])**2)

    def path_cost(path):
        return len(path) - 1

    def a_star_manhattan(self):
        return self.a_star(self.manhattan)
    
    def a_start_euclidean(self):
        return self.a_star(self.euclidean)

    def a_star(self, h):
        self.is_running = False  # Stop any ongoing search
        self.is_running = True
        self.reset_maze()
        frontier = [[[self.start], 0]]
        visited = [self.start]
        while frontier and self.is_running:
            frontier = sorted(frontier, key=lambda x : x[1])
            path, cost = frontier.pop(0)

            pos = path[-1]
            self.maze[pos[0]][pos[1]] = PLAYER
            self.update_interface()

            if np.array_equal(self.exit, pos):
                self.is_running = False
                return path, visited
            
            self.maze[pos[0]][pos[1]] = PATH

            neighbors = self.get_neighbors(pos)
            for n in neighbors:
                if not(any(np.array_equal(n, v) for v in visited)):

                    if not(any(np.array_equal(n, v) for v in visited)):
                        visited.append(n)

                    new_path = path + [n]
                    new_cost = h(n)
                    frontier.append([new_path, new_cost])

        self.is_running = False
        return None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = Maze(30, 30, root)
    root.mainloop()

