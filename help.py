import tkinter as tk
import queue

# Define the maze as a grid
maze = [
    ["S", "0", "1", "1", "1", "1", "1"],
    ["1", "0", "0", "0", "0", "0", "1"],
    ["1", "0", "1", "1", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "E"],
    ["1", "1", "1", "0", "1", "1", "1"]
]

# Directions for movement in the maze
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(maze):
    start = find_start(maze)
    stack = [(start, [start])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        if maze[x][y] == "E":
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            for direction in directions:
                nx, ny = x + direction[0], y + direction[1]
                if is_valid_move(maze, nx, ny, visited):
                    stack.append(((nx, ny), path + [(nx, ny)]))
    return []

def bfs(maze):
    start = find_start(maze)
    q = queue.Queue()
    q.put((start, [start]))
    visited = set()

    while not q.empty():
        (x, y), path = q.get()
        if maze[x][y] == "E":
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            for direction in directions:
                nx, ny = x + direction[0], y + direction[1]
                if is_valid_move(maze, nx, ny, visited):
                    q.put(((nx, ny), path + [(nx, ny)]))
    return []

def find_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                return (i, j)
    return None

def is_valid_move(maze, x, y, visited):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != "1" and (x, y) not in visited

def display_solution(path):
    for x, y in path:
        maze[x][y] = "*"
    for row in maze:
        print(" ".join(row))

# Display the maze
def display_maze(canvas):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            color = "white"
            if maze[i][j] == "1":
                color = "black"
            elif maze[i][j] == "S":
                color = "green"
            elif maze[i][j] == "E":
                color = "red"
            elif maze[i][j] == "*":
                color = "yellow"
            canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill=color, outline="gray")

# Main application class
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.canvas = tk.Canvas(root, width=280, height=200)
        self.canvas.pack()

        self.dfs_button = tk.Button(root, text="Solve with DFS", command=self.solve_dfs)
        self.dfs_button.pack(side="left")
        
        self.bfs_button = tk.Button(root, text="Solve with BFS", command=self.solve_bfs)
        self.bfs_button.pack(side="right")
        
        display_maze(self.canvas)
        
    def solve_dfs(self):
        path = dfs(maze)
        display_solution(path)
        self.canvas.delete("all")
        display_maze(self.canvas)
    
    def solve_bfs(self):
        path = bfs(maze)
        display_solution(path)
        self.canvas.delete("all")
        display_maze(self.canvas)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
